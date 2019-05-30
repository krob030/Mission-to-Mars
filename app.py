# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

mongo = PyMongo(app)

# create route that renders index.html template
@app.route("/")
def index():
    mission_to_mars = mongo.db.mission_to_mars.find_one()
    return render_template("index.html", mission_to_mars=mission_to_mars)

@app.route("/scrape")
def scrape():
    mission_to_mars = mongo.db.mission_to_mars
    mission_to_mars_data= scrape_mars.scrape()
    mission_to_mars_data.update({}, mission_to_mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)