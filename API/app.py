import flask
import datetime
import folium
import rdflib as rdf

app = flask.Flask(__name__)

cities = {"Lyon":{"coord":(45.764043,4.835659)}}

query = {
    "PREFIX":"D:\\Thomas\\Etude\\ESILV\\A8\\Web_datamining_and_semantics\\Projet\\Github\\project_velos_lyon\\data\\rdf_files\\bicycle_test.rdf",
    "all_open_station":"""
    PREFIX ns0: <http://www.semanticweb.org/adrie/ontologies/Projet#>
    SELECT ?x ?y ?z WHERE
    {
        ?x ?y ?z .
        ?x ns0:status 'OPEN'
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
    g.load("D:\\Thomas\\Etude\\ESILV\\A8\\Web_datamining_and_semantics\\Projet\\Github\\project_velos_lyon\\data\\rdf_files\\bicycle_lyon.rdf")

    print(len(g))

    count = 0

    for s, p, o in g:
        count += 1
        print(s,p,o)
        if count > 5:
            break

    q = """
    SELECT ?x ?y ?z
    WHERE {
        ?x ?y ?z .
        ?x ns0:status 'OPEN' .
    }"""
    
    response_query = g.query(q)

    to_jsonify = ""

    print(len(response_query))

    for row in response_query:
        print("row :", row)
        to_jsonify += "<p>" + row.s + " " + row.p + " " + row.o + "</p>"
    print()
    print("response_query :", response_query)
    print()
    print("to_jsonify :", to_jsonify)
    return flask.render_template('lyon.html', display=to_jsonify)

@app.route("/city/<city>")
def fetch_city(city):
    g = rdf.Graph()
    g.load(query['PREFIX'])

    q = query['all_open_station']
    response_query = g.query(q)

    to_jsonify = ""

    for row in response_query:
        to_jsonify += "<p>" + row.s + " " + row.p + " " + row.o + "</p>"
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
    
    app.run(debug=True, reload=True)