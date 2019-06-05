# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
#import pymongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

#client = pymongo.MongoClient(conn)
#mongo = PyMongo(app)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
# connect to mongo db
#db = client.mission_to_mars

# create route that renders index.html template
@app.route("/")
def index():
    mission_to_mars = mongo.db.mission_to_mars.find_one()
    return render_template("index.html", mission_to_mars=mission_to_mars)

@app.route("/scrape")
def scrape():
    mission_to_mars = mongo.db.mission_to_mars
    mission_to_mars_data= scrape_mars.scrape()
    mission_to_mars.update({}, mission_to_mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)