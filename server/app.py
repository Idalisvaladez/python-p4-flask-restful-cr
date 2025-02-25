#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API"
        }
        return make_response(response_dict, 200)
api.add_resource(Home, '/')

class Newsletters(Resource):
    def get(self):
        newsletters = [news.to_dict() for news in Newsletter.query.all()]
        return make_response(newsletters, 200)
    
    def post(self):
        new_news = Newsletter(
            title = request.form['title'],
            body = request.form['body'],
        )
        db.session.add(new_news)
        db.session.commit()

        return make_response(new_news.to_dict(), 200)
    
api.add_resource(Newsletters, '/newsletters')

class NewsletterById(Resource):

    def get(self, id):
        newsletter = Newsletter.query.filter_by(id = id).first()

        return make_response(newsletter.to_dict(), 200)
api.add_resource(NewsletterById, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
