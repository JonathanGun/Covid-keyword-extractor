import re
from flask import Flask, flash, redirect, url_for, render_template
from forms import MyForm
from string_matcher import StringMatcher, BoyerMoore, KMP, Regex

app = Flask(__name__)

algorithm_map = {
    "boyer-moore": BoyerMoore(),
    "kmp": KMP(),
    "regex": Regex(),
}


def parse_sentence(text: str):
    split_article_content = []
    for element in text:
        split_article_content += re.split("(?<=[.!?])\s+", element)
    return split_article_content


@app.route('/', methods=['GET', 'POST'])
def home():
    form = MyForm()
    keywords = form.keyword.data
    if keywords:
        keywords = keywords.split(',')
    files = form.upload_files.data
    if form.validate_on_submit():
        if files:
            for file in files:
                if file.mimetype != 'text/plain':
                    flash(f"Please upload only text files", "danger")
                    return redirect(url_for("home", form=MyForm()))
            flash(f"{len(files)} file(s) submitted with keywords: {keywords}", "success")
            flash(f"File names: {[file.filename for file in files]}", "success")
            flash(f'Algorithm: { form.algorithm.data}', "success")

            stringMatcher = StringMatcher(algorithm_map[form.algorithm.data])
            for file in files:
                text = "".join(list(x.decode("utf-8").rstrip("\r\n").rstrip("\n") for x in file.readlines()))
                for sentence in text.split("."):
                    for keyword in keywords:
                        idx = stringMatcher.match(sentence, keyword)
                        if idx != -1:
                            print(sentence)
                            print()
                            break

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.config['SECRET_KEY'] = 'd4b0321f7bf962215a0dd420459c1044'
    app.run(debug=True)
