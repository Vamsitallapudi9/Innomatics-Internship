import re
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Startpage.html')

@app.route('/result', methods=['POST'])
def result():
    pattern = request.form.get('pattern')
    text = request.form.get('text')
    matches = re.findall(pattern, text)
    return render_template('Result.html', pattern=pattern, text=text, matches=matches)

if __name__ == '__main__':
    app.run(debug=False)
