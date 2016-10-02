from meta import search_games_ps_store
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)



class searchEndpoint(Resource):
	def get(self, query):
		return search_games_ps_store(query)

api.add_resource(searchEndpoint, '/<string:query>')

if __name__ == '__main__':
    app.run(debug=True)