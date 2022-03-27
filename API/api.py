import flask
import datetime
import folium

app = flask.Flask(__name__)

@app.context_processor
def inject_now():
    now = datetime.datetime.now().strftime("%d %B %Y")
    return dict(now=now)

@app.route("/")
def index():
    return flask.render_template('index.html')

@app.route("/city")
def city():
    coord = (45.764043, 4.835659)
    f_map = folium.Map(location=coord)
    return flask.render_template('city.html',city="Lyon", f_map=f_map._repr_html_())

@app.route("/lyon")
def lyon():
    return flask.render_template('lyon.html')

@app.route("/city/<city>")
def fetch_city(city):
    to_jsonify = {"main" : "Hello " + city + " !"}
    return flask.jsonify(to_jsonify)

if __name__ == "__main__":
    
    app.run(debug=True)