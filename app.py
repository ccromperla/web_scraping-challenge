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
    mars_data = mongo.db.marsData.find_one()
    return render_template("index.html", mars=mars_data)


@app.route("/scrape")
def scrape():
    # Refer to db collection 
    marsTable = mongo.db.marsData

    # If it exists drop it
    mongo.db.marsData.drop()

    # Call scrape mars script
    mars_data = scrape_mars.scrape_all()

    # Take dictionary and load it into mondgoDB
    marsTable.insert_one(mars_data)

    # Return to the index route
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)