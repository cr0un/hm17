# app.py

from flask import request
from flask_restx import Api, Resource
from marshmallow import Schema, fields
from create_data import *
from config import app
from create_data import Director


class Movie_Schema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    director_id = fields.Int()
    genre_id = fields.Int()

    #тестовая функция для вывода имени режиссера, по мимо его id.
    name = fields.Method("get_director_name")
    def get_director_name(self, obj):
        director = Director.query.filter_by(id=obj.director_id).first()
        return director.name


class Director_Schema(Schema):
    id = fields.Int()
    name = fields.Str()


class Genre_Schema(Schema):
    id = fields.Int()
    name = fields.Str()


api = Api(app)

movie_ns = api.namespace("movies")
director_ns = api.namespace("director")
genge_ns = api.namespace("genre")

movie_schema = Movie_Schema()
movies_schema = Movie_Schema(many=True)

director_schema = Director_Schema()
directors_schema = Director_Schema(many=True)

genre_schema = Genre_Schema()
genres_schema = Genre_Schema(many=True)


@movie_ns.route("/")
class Movies_view(Resource):
    def get(self, page=1):
        movies_query = db.session.query(Movie)

        director_id = request.args.get("director_id")
        if director_id is not None:
            movies_query = movies_query.filter(Movie.director_id == director_id)

        genre_id = request.args.get("genre_id")
        if genre_id is not None:
            movies_query = movies_query.filter(Movie.genre_id == genre_id)

        movies = movies_query.paginate(page, per_page=5)
        return movies_schema.dump(movies.items), 200


    def post(self):
        req_json = request.json
        if req_json:
            new_movie = Movie(**req_json)
            with db.session.begin():
                db.session.add(new_movie)
            return "", 201
        else:
            return "Invalid JSON data",


@movie_ns.route("/<int:uid>")
class Movie_view(Resource):
    def get(self, uid: int):
        movie_query = db.session.query(Movie).get(uid)
        if not movie_query:
            return "", 404
        return movie_schema.dump(movie_query), 200


    def put(self, uid: int):
        updated_rows = db.session.query(Movie).filter(Movie.id == uid).update(request.json)

        if updated_rows != 1:
            return "", 400

        db.session.commit()
        return "", 204


    def delete(self, uid: int):
        delete_rows = db.session.query(Movie).get(uid)

        if not delete_rows:
            return "", 400

        db.session.delete(delete_rows)
        db.session.commit()

        return "", 204


@director_ns.route("/")
class Directors_view(Resource):
    def get(self):
        directors_all = db.session.query(Director)
        return directors_schema.dump(directors_all), 200


    def post(self):
        req_json = request.json
        if req_json:
            new_director = Movie(**req_json)
            with db.session.begin():
                db.session.add(new_director)
            return "", 201
        else:
            return "Invalid JSON data",


@director_ns.route("/<int:uid>")
class Director_view(Resource):
    def get(self, uid):
        director_query = db.session.query(Director).get(uid)
        if not director_query:
            return "", 404
        return director_schema.dump(director_query), 200


    def put(self, uid:int):
        updated_rows = db.session.query(Director).filter(Director.id == uid).update(request.json)

        if updated_rows != 1:
            return "", 404

        db.session.commit()
        return "", 204


    def delete(self, uid: int):
        delete_rows = db.session.query(Director).get(uid)

        if not delete_rows:
            return "", 400

        db.session.delete(delete_rows)
        db.session.commit()

        return "", 204


@genge_ns.route("/")
class Genres_view(Resource):
    def get(self):
        genres_all = db.session.query(Genre)
        return genres_schema.dump(genres_all), 200


    def post(self):
        req_json = request.json
        if req_json:
            new_genre = Movie(**req_json)
            with db.session.begin():
                db.session.add(new_genre)
            return "", 201
        else:
            return "Invalid JSON data",


@genge_ns.route("/<int:uid>")
class Genre_view(Resource):
    def get(self, uid):
        genre_query = db.session.query(Genre).get(uid)
        if not genre_query:
            return "", 404
        return director_schema.dump(genre_query), 200


    def put(self, uid:int):
        updated_rows = db.session.query(Genre).filter(Genre.id == uid).update(request.json)

        if updated_rows != 1:
            return "", 404

        db.session.commit()
        return "", 204


    def delete(self, uid: int):
        delete_rows = db.session.query(Genre).get(uid)

        if not delete_rows:
            return "", 400

        db.session.delete(delete_rows)
        db.session.commit()

        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
