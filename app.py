from flask import Flask
from flask import render_template, request
from bfs import bfs


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "GET":
		connection_result_list=[]
		return render_template( "index.html", connection_result_list=connection_result_list)
	if request.method == "POST":
		req = request.form
		player_one, player_two =  req["PlayerOne"], req["PlayerTwo"]
		connection_result, connection_result_list = bfs(player_one, player_two)
		return render_template( "index.html", connection_result_list=connection_result_list)


if __name__ == '__main__':
	app.run(debug=True)
