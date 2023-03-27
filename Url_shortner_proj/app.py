import os,random,string
from flask import Flask,render_template ,request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from validators import url as validate_url

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


class Url(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.Text)
    short_url = db.Column(db.Text)

    def __init__(self, long_url, short_url):
        self.long_url = long_url
        self.short_url = short_url


def shortURL(size):
    combination=string.ascii_letters + string.digits
    return (''.join(random.choices(combination, k=size)))


@app.route('/', methods=["GET", "POST"])
def Home():
    if request.method == "POST":
        Original_link = request.form.get('url')
        New_link = Url.query.filter_by(long_url=Original_link).first()
        if New_link:
            return render_template('home.html', error=0, finalurl=New_link.short_url)
        elif validate_url(Original_link):
            while True:
                shorturl = shortURL(5)
                if not Url.query.filter_by(short_url=shorturl).first():
                    db.session.add(Url(Original_link, shorturl))
                    db.session.commit()
                    return render_template('home.html', error="valid", finalurl=shorturl)
        else:
            return render_template('home.html', error="not valid")
    return render_template("home.html")



@app.route('/history', methods=["GET", "POST"])
def History():
    nlinks = Url.query.all()
    return render_template("history.html", saved=nlinks)


@app.route('/<finalurl>')
def redirection(finalurl):
    redirecturl = Url.query.filter_by(short_url=finalurl).first()
    if redirecturl:
        return redirect(redirecturl.long_url)
    else:
        return f"<h1>URL doesn't Exist</h1>"


@app.route('/delete/<int:id>')
def delete(id):
    item = Url.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect('/history')


if __name__ == "__main__":
    app.run(debug=True)