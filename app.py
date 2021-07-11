from flask import Flask
from flask import render_template, request
from bfs import bfs


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
	headers = {'X-Auth-Token': 'f7a3c3dfbeb2432dbe0c65ae886c2d45'}
	url = 'http://api.football-data.org/v2/teams'
	teams_data = requests.get(url, headers=headers)
	return teams_data

if __name__ == '__main__':
	app.run(debug=True)
