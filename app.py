# Simple fullstack web application built using flask framework having a SQLite database and SQLAlchemy is the package used for 
# facilitating the communication between the application and the database.
'''In this application we are displaying the list of articles that we have in our database'''
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.sqlite3'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

#Models
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    articles= db.relationship("Article", secondary="article_authors")


class Article(db.Model):
    __tablename__ = 'article'
    article_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    authors = db.relationship("User", secondary="article_authors")


class ArticleAuthors(db.Model):
    __tablename__ = 'article_authors'
    user_id = db.Column(db.Integer,   db.ForeignKey(
        "user.user_id"), primary_key=True, nullable=False)
    article_id = db.Column(db.Integer,  db.ForeignKey(
        "article.article_id"), primary_key=True, nullable=False)


#Controllers
@app.route('/', methods=['POST', 'GET'])
def articles():
    articles = Article.query.all()
    return render_template("articles.html", articles=articles)


@app.route("/articles_by/<username>", methods=["GET", "POST"])
def articles_by_author(username):
    if request.method == "GET":
        articles = Article.query.filter(Article.authors.any(username=username))
        return render_template("articles_by_author.html", articles=articles,author=username)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
