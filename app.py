import os
from flask import Flask, flash, request, render_template
from forms import MyForm
import requests
from bs4 import BeautifulSoup
from string_matcher import StringMatcher, BoyerMoore, KMP, Regex
from extractor import Extractor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['UPLOAD_FOLDER'] = '/tmp'

algorithm_map = {
    "boyer_moore": BoyerMoore(),
    "kmp": KMP(),
    "regex": Regex(),
}


def get_article(url) -> str:
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c, features="html.parser")

    article_text = []
    article = soup.findAll("div")
    for div in article:
        for p in div.findAll("p"):
            article_text.append('\n' + ''.join(p.findAll(text=True)))
    return "\n".join(dict.fromkeys(article_text))


def readfile(file) -> str:
    text = ""
    for line in "".join(list(x.decode("utf-8").replace('\r', '') for x in file.readlines())).split("\n"):
        if line:
            text += line
            text += ". " if line[-1] != "." else " "
    return text


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
    ] (default: files-1..n),
    "algorithm": "boyer_moore" # or "kmp" or "regex" (default: "regex")
    "allow_weak" : "True" (default: "False")
}
"""


@app.route('/extractor', methods=['GET', 'POST'])
def extractor():
    form = MyForm()
    if request.method == "GET":
        return render_template("extractor.html", form=form)

    keywords = []
    algorithm = "regex"
    filenames = []
    texts = []
    allow_weak = False

    if request.method == "POST":
        if form.validate_on_submit():
            print("from user POST")
            keywords = form.keyword.data.split(',')
            algorithm = form.algorithm.data
            files = form.upload_files.data
            allow_weak = form.allow_weak.data
            if form.text.data:
                texts.append(form.text.data)

            elif form.link.data:
                try:
                    texts.append(get_article(form.link.data))
                    filenames.append(form.link.data)
                except Exception:
                    return render_template("extractor.html", form=form)

            elif files:
                print(files)
                for file in files:
                    if file.mimetype == 'text/plain':
                        texts.append(readfile(file))
                        filenames.append(file.filename)
                    else:
                        flash(f"Please upload only text files", "danger")
                        return render_template("extractor.html", form=form)
        else:
            print("from POST API")
            keywords = request.values.getlist('keywords')
            texts = request.values.getlist('texts')
            try:
                filenames = request.values.getlist('filenames')
            except KeyError:
                pass
            try:
                algorithm = request.values["algorithm"]
            except KeyError:
                pass
            try:
                allow_weak = request.values["allow_weak"]
            except KeyError:
                pass

    try:
        stringMatcher = StringMatcher(algorithm_map[algorithm])
        results = []
        for i in range(len(texts)):
            result = {}
            try:
                result["filename"] = filenames[i]
            except IndexError:
                result["filename"] = "file-" + str(i) + ".txt"
            result["matches"] = Extractor(keywords=keywords, matcher=stringMatcher).extract(texts[i], allow_weak)
            result["count"] = {
                "total": len(result["matches"]),
                "weak": len(list(match for match in result["matches"] if match.weak)),
            }
            results.append(result)
        if results:
            return render_template("result.html", results=results)

    except Exception:
        pass

    return render_template("extractor.html", form=form)


@app.route('/sample/<filename>.txt')
def send_text_file(filename):
    """Send your static text file."""
    return app.send_static_file(filename + '.txt')


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html', title="Page Not Found"), 404


if __name__ == "__main__":
    app.run(debug=True)
