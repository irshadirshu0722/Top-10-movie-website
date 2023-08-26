from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

from flask_sqlalchemy import SQLAlchemy

# import sqlite3
# dp = sqlite3.connect("Movies_database.db")


class Edit(FlaskForm):
    rating = StringField("rating",[DataRequired()])
    review = StringField("review", [DataRequired()])
    submit = SubmitField("submit")

class Add(FlaskForm):
    name = StringField("name",[DataRequired()])

    submit = SubmitField("Add movie")

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Movies_database.db"
db=SQLAlchemy()
db.init_app(app)

class Movies(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(250),nullable=False)
    year = db.Column(db.Integer,nullable=False)
    description=db.Column(db.String(1000),nullable=False)
    rating = db.Column(db.Float,nullable=False)
    ranking = db.Column(db.Integer,nullable=False)
    review = db.Column(db.String(250),nullable=False)
    img = db.Column(db.String(250),nullable=False)

    def __repr__(self):
        return f"<Book{self.title}>"
# with app.app_context():
#     db.create_all()


# with app.app_context():
#     new_movie = Movies(
#         title="Phone Booth",
#         year=2002,
#         description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#         rating=7.3,
#         ranking=10,
#         review="My favourite character was the caller.",
#         img="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#     )
#     db.session.add(new_movie)
#     db.session.commit()


# with app.app_context():
#     movie = db.get_or_404(Movies, 8)
#     # with app.app_context():
#     db.session.delete(movie)
#     db.session.commit()


# with app.app_context():
#     movie = db.session.execute(db.select(Movies).filter_by(id=2)).scalar_one()
#     db.session.delete(movie)
#     db.session.commit()


# with app.app_context():
#     movie = db.session.execute(db.select(Movies).filter_by(id=1)).scalar_one()
#     movie.title="title"
#     db.session.commit()
import requests

url = "https://www.omdbapi.com/"







@app.route("/")
def home():
    result = db.session.execute(db.select(Movies).order_by(Movies.rating))
    all_movies = result.scalars().all()  # convert ScalarResult to Python List

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()


    return render_template("index.html",movies=all_movies)
@app.route('/<int:id>/edit',methods=["POST","GET"])
def edit(id):

    edit_form=Edit()
    if edit_form.validate_on_submit():
        with app.app_context():
            movie = db.session.execute(db.select(Movies).filter_by(id=id)).scalar_one()
            movie.rating=edit_form.rating.data
            movie.review = edit_form.review.data
            db.session.commit()
            return redirect("/")



    with app.app_context():
        movie = db.session.execute(db.select(Movies).filter_by(id=id)).scalar_one()
    return render_template("edit.html",form=edit_form,movie=movie)
@app.route('/<int:id>/delete')
def delete(id):
    with app.app_context():
        movie = db.session.execute(db.select(Movies).filter_by(id=id)).scalar_one()
        db.session.delete(movie)
        db.session.commit()
        return redirect("/")
@app.route('/add',methods=["POST","GET"])
def add_movie():
    add = Add()
    if add.validate_on_submit():
        title = add.name.data
        response = requests.get(url, params={"apikey":"5af83878","t":title})
        print(response.status_code)
        if response.status_code==200:
            with app.app_context():
                movies_all = Movies.query.all()
            ranking = 9-len(movies_all)
            print(len(movies_all))
            data=response.json()

            with app.app_context():
                new_movie = Movies(
                    title=data['Title'],
                    year=data['Year'],
                    description=data['Plot'],
                    rating=0,
                    ranking=ranking+1,
                    review="",
                    img=data['Poster']
                )
                db.session.add(new_movie)
                db.session.commit()
        return redirect('/')

    return render_template("add.html",form=add)
if __name__ == '__main__':
    app.run(debug=True)
