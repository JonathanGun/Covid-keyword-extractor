import os
from flask import Flask, flash, request, render_template
from forms import MyForm
from string_matcher import StringMatcher, BoyerMoore, KMP, Regex
from extractor import Extractor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

algorithm_map = {
    "boyer_moore": BoyerMoore(),
    "kmp": KMP(),
    "regex": Regex(),
}


def readfile(file) -> str:
    return "".join(list(x.decode("utf-8").rstrip("\r\n").rstrip("\n") for x in file.readlines()))


@app.route('/')
def index():
    return render_template("index.html")


"""
example POST:
{
    "keywords": ["terindikasi positif", "orang", "kasus positif"],
    "texts" : [
        "this is a very long text containing the article that you want to send to us. Our program will match the keyword within your text and extract useful information from it.",
        "this is the second article that you want to analize",
        "you can submit as many file as you want",
        "but all of them must in text file"
    ],
    "filenames": [
        "covid-19-indonesia.txt",
        "i only supply two filenames.txt"
    ] # optional (default: 1..n),
    "algorithm": "boyer-moore" # or "kmp" or "regex" (default: "regex")
}
"""


@app.route('/extractor', methods=['GET', 'POST'])
def extractor():
    form = MyForm()
    if request.method == "GET":
        return render_template("extractor.html", form=form)

    keywords = []
    algorithm = ""
    filenames = []
    texts = []

    if request.method == "POST":
        if form.validate_on_submit():
            keywords = form.keyword.data.split(',')
            algorithm = form.algorithm.data
            files = form.upload_files.data
            if files:
                for file in files:
                    if file.mimetype == 'text/plain':
                        texts.append(readfile(file))
                        filenames.append(file.filename)
            if len(filenames) == 0:
                flash(f"Please upload only text files", "danger")
                return render_template("extractor.html", form=form)
        else:
            keywords = request.values.getlist('keywords')
            texts = request.values.getlist('texts')
            filenames = request.values.getlist('filenames')
            algorithm = request.values["algorithm"]

    try:
        print(keywords)
        print(texts)
        print(algorithm)
        stringMatcher = StringMatcher(algorithm_map[algorithm])
        results = []
        for i in range(len(texts)):
            result = {}
            try:
                result["filename"] = filenames[i]
            except IndexError:
                result["filename"] = "file-" + str(i) + ".txt"
            result["matches"] = Extractor(keywords=keywords, matcher=stringMatcher).extract(texts[i])
            results.append(result)
        if results:
            return render_template("result.html", results=results, len=len(results))

    except Exception:
        pass

    return render_template("extractor.html", form=form)


@app.route('/sample/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html', title="Page Not Found"), 404


if __name__ == "__main__":
    app.run(debug=True)
