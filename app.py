# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------
from flask import Flask, jsonify, redirect, render_template
import pymongo                                   #Python driver for Mongo
from pymongo import MongoClient
# import scrape_mars
import scrape_mars

# --------------------------------------------------------------------------
# Client initializes logical session for ordering sequential operations
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Creates a flask instance folder where flask will autodetect folder location
# Alternatively, specify absolute path, but it would leave no room for error
# --------------------------------------------------------------------------
app = Flask(__name__)

# --------------------------------------------------------------------------
# dictionary style access to collection
# --------------------------------------------------------------------------
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.mars_data_DB
mars_collection = db.mars_collection

# --------------------------------------------------------------------------
# Initializes default route
# --------------------------------------------------------------------------
@app.route("/")
def render_index():
    # Error handler for missing collection
    try:
        mars_find =  mars_collection.find_one()

        # Distributes data from collection
        news_title = mars_find['news_data']['news_title']
        paragraph_text_1 = mars_find['news_data']['paragraph_text_1']
        paragraph_text_2 = mars_find['news_data']['paragraph_text_2']
        featured_image_url = mars_find['featured_image_url']
        mars_weather_tweet = mars_find['mars_weather']
        mars_facts_table = mars_find['facts_table']
        hemisphere_title_1 = mars_find['hemishpere_image_urls'][0]['title']
        hemisphere_img_1 = mars_find['hemishpere_image_urls'][0]['img_url']
        hemisphere_title_2 = mars_find['hemishpere_image_urls'][1]['title']
        hemisphere_img_2 = mars_find['hemishpere_image_urls'][1]['img_url']
        hemisphere_title_3 = mars_find['hemishpere_image_urls'][2]['title']
        hemisphere_img_3 = mars_find['hemishpere_image_urls'][2]['img_url']
        hemisphere_title_4 = mars_find['hemishpere_image_urls'][3]['title']
        hemisphere_img_4 = mars_find['hemishpere_image_urls'][3]['img_url']
    except (IndexError, TypeError) as error_handler:

        # Missing collection; clears fields
        news_title = ""
        paragraph_text_1 =""
        paragraph_text_2 = ""
        featured_image_url = ""
        mars_weather_tweet = ""
        mars_facts_table = ""
        hemisphere_title_1 = ""
        hemisphere_img_1 = ""
        hemisphere_title_2 = ""
        hemisphere_img_2 = ""
        hemisphere_title_3 = ""
        hemisphere_img_3 = ""
        hemisphere_title_4 = ""
        hemisphere_img_4 = ""

    # ------------------------------------------------------------------------
    # Renders template to index.html
    # ------------------------------------------------------------------------
    return render_template("index.html", news_title=news_title,\
                                         paragraph_text_1=paragraph_text_1,\
                                         paragraph_text_2=paragraph_text_2,\
                                         featured_image_url=featured_image_url,\
                                         mars_weather_tweet=mars_weather_tweet,\
                                         mars_facts_table=mars_facts_table,\
                                         hemisphere_title_1=hemisphere_title_1,\
                                         hemisphere_img_1=hemisphere_img_1,\
                                         hemisphere_title_2=hemisphere_title_2,\
                                         hemisphere_img_2=hemisphere_img_2,\
                                         hemisphere_title_3=hemisphere_title_3,\
                                         hemisphere_img_3=hemisphere_img_3,\
                                         hemisphere_title_4=hemisphere_title_4,\
                                         hemisphere_img_4=hemisphere_img_4)

# --------------------------------------------------------------------------
# Initializes scrape route; inserts results into  mars_data_DB in MongoDB
# --------------------------------------------------------------------------
@app.route('/scrape')
def scrape_mars_data():
    # tumi_mars = client.db.tumi_mars
    scrape_results = scrape_mars.scrape()
    mars_collection.replace_one({}, scrape_results, upsert=True)
    return redirect('http://localhost:5000/login/authorized', code=302)

if __name__ == '__main__':
    app.run(debug=True)