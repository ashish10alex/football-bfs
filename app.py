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
		connection_result = bfs(player_one, player_two)
		return render_template( "index.html", connection_result=connection_result)


if __name__ == '__main__':
	app.run(debug=True)
