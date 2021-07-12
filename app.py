import os
from flask import Flask
from flask import render_template, request
from bfs import bfs

api_key = os.environ.get('FOOTBALL_API_KEY')


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "GET":
		return render_template( "index.html")
	if request.method == "POST":
		req = request.form
		player_one, player_two =  req["PlayerOne"], req["PlayerTwo"]
		connection_result_list = bfs(player_one, player_two)
		return render_template( "index.html", connection_result_list=connection_result_list)

def get_images():
	headers = {'X-Auth-Token': api_key}
	url = 'http://api.football-data.org/v2/teams'
	teams_data = requests.get(url, headers=headers)
	return teams_data

if __name__ == '__main__':
	app.run(debug=True)
