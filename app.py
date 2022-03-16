from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")


@app.route("/")
def index():
    # listings = mongo.db.listings.find_one()
    # return render_template("index.html", listings=listings)

    return('Hello World')


@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_all()
    # print(mars_data)

    return mars_data
    # listings = mongo.db.listings
    # listings_data = scrape_mars.scrape()
    # listings.update_one({}, {"$set": listings_data}, upsert=True)
    # return redirect("/", code=302)


if __name__ == "__main__":
    app.run()