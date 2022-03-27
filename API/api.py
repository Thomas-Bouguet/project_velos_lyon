import flask
import datetime
import folium
import rdflib as rdf

app = flask.Flask(__name__)

cities = {"Lyon":{"coord":(45.764043,4.835659)}}

query = {
    "PREFIX":"http://www.semanticweb.org/adrie/ontologies/Projet#",
    "all_open_station":"""
    SELECT ?name WHERE 
    {
        ?x velo:status 'OPEN'.
        ?x velo:name_station ?name.
    }
    """,
    "all_lat":"""
    SELECT ?lat WHERE 
    {
        ?x rdf:type velo:Bicycle_station.
        ?x velo:lat_station ?lat.
    }
    """,
    "all_lon":"""
    SELECT ?lon WHERE 
    {
        ?x rdf:type velo:Bicycle_station.
        ?x velo:lon_station ?lon.
    }
    """,
    "five_more_stands":"""
    SELECT ?station WHERE
    {
        ?station rdf:type velo:Bicycle_station.
        ?station velo:available_bike_stands ?available.
        FILTER(?available > 5).
    }
    """
}

@app.context_processor
def inject_now():
    now = datetime.datetime.now().strftime("%d %B %Y")
    return dict(now=now)

@app.route("/")
def index():
    return flask.render_template('index.html')

@app.route("/city")
def city():
    return flask.render_template('city.html',city="Lyon")

@app.route("/lyon")
def lyon():
    g = rdf.Graph()
    g.parse(query['PREFIX'])

    response_query = g.query(query['all_lat'])

    to_jsonify = response_query
    return flask.render_template('lyon.html')

@app.route("/city/<city>")
def fetch_city(city):
    g = rdf.Graph()
    g.parse(query['PREFIX'])

    response_query = g.query(query['all_lat'])

    to_jsonify = response_query
    #to_jsonify = {"main" : "Hello " + city + " !"}
    
    return to_jsonify

@app.route("/maps/france")
def display_france_map():
    coord = (46.539758, 2.430331)
    f_map = folium.Map(location=coord,zoom_start=5.2)
    for key,val in cities.items():
        folium.CircleMarker(
            location = (val["coord"]),
            radius = 10,
            color = 'crimson',
            fill = True,
            fill_color = 'crimson',
            tooltip = key,
            width = 100,
            popup = folium.Popup("<a href=/" + key.lower() + " target='_blank'>Go to " + key + "</a>",min_width=60,max_width=60)
        ).add_to(f_map)
    return f_map._repr_html_()

@app.route("/maps/lyon")
def display_lyon_map():
    coord = cities['Lyon']['coord']
    f_map = folium.Map(location=coord,zoom_start=12)
    return f_map._repr_html_()

if __name__ == "__main__":
    
    app.run(debug=True)