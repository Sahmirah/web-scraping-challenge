from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    
    # find one document from our mongo db and return it.
    mars_data = mongo.db.mars_data.find_one()
    
    # pass that listing to render_template
    return render_template("index.html", mars_data=mars_data)

# set our path to trigger our scrape
@app.route("/scrape")
def scrape():
    
    #Create a listings database
    mars_data = mongo.db.mars_data

    # call the scrape function in our scrape_mars file. This will scrape and save to mongo.
    listings_data = scrape_mars.scrape()

    # update our listings with the data that is being scraped.
    mars_data.update({}, listings_data, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)