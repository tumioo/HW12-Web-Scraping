# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------
import numpy as np
import pandas as pd
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup
import requests as req
import time
# --------------------------------------------------------------------------
# Initialize firefox browser for the test with sleep timer for loading
# --------------------------------------------------------------------------
def initBrowser():
    return Browser("chrome", headless=False)
    time.sleep(10)

# --------------------------------------------------------------------------
# Close splinter Browser object (DRY)
# --------------------------------------------------------------------------
def closeBrowser(browser):
    browser.quit()
    time.sleep(10)

# --------------------------------------------------------------------------
# Create python script  called mars_scrape from Jupyter notebook code
# The script will create a dictionary of all your scraped data 
# --------------------------------------------------------------------------
def scrape(): #this is my scrape function def defines a function
    mars_data = {}

    mars_data["news_data"] = marsNewsData()

    mars_data["featured_image_url"] = marsFeaturedImageURL()

    mars_data["mars_weather"] = marsWeather()

    mars_data["facts_table"] = marsFacts()

    mars_data["hemishpere_image_urls"] = marsHemisphereImageURLs()

    return mars_data

# --------------------------------------------------------------------------
# NASA Mars News - scrape latest article from Nasa news site
# Keep Title and paragraph
# --------------------------------------------------------------------------
def marsNewsData():
    news_data = {}
    paragraph_text = []
    browser=Browser("chrome")
    main_url = "https://mars.nasa.gov/"                                    
    nasa_url = "https://mars.nasa.gov/news/"                          
    
    browser.visit(nasa_url)
    time.sleep(5)
    nasa_soup = BeautifulSoup(browser.html, 'html.parser')
    soup_div = nasa_soup.find(class_="slide")
    soup_news = soup_div.find_all('a')
    news_title = soup_news[1].get_text().strip()
    soup_p = soup_div.find_all('a', href=True)
    soup_p_url = soup_p[0]['href']
    browser.visit("https://mars.nasa.gov/")
    para_soup = BeautifulSoup(browser.html, "html.parser")
    ww_paragraphs = para_soup.find(class_='wysiwyg_content')
    paragraphs = ww_paragraphs.find_all('p') 
    for paragraph in paragraphs:
        clean_paragraph = paragraph.get_text().strip()
        paragraph_text.append(clean_paragraph)

    news_data["news_title"] = news_title
    news_data["paragraph_text_1"] = paragraph_text[0]
    news_data["paragraph_text_2"] = paragraph_text[1]
    return news_data
# --------------------------------------------------------------------------
# JPL Mars Space Images - Visit the url for JPL's Featured Space Image.
# Use splinter to navigate the site and find the image url for the current
# Featured Mars Image and assign the url string to a variable called
# featured_image_url.
# --------------------------------------------------------------------------
def marsFeaturedImageURL():
    browser = initBrowser()

    jpl_fullsize_url = 'https://photojournal.jpl.nasa.gov/jpeg/'
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    time.sleep(5)
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')
    time.sleep(5)
    featured_image_list=[]
    for image in jpl_soup.find_all('div',class_="img"):
        featured_image_list.append(image.find('img').get('src'))

    feature_image = featured_image_list[0]
    temp_list_1 = feature_image.split('-')
    temp_list_2 = temp_list_1[0].split('/')
    featured_image_url = jpl_fullsize_url + temp_list_2[-1] + '.jpg'
    return featured_image_url

# --------------------------------------------------------------------------
# Mars Weather - Visit the Mars Weather twitter account and scrape the
# latest Mars weather tweet from the page. Save the tweet text for the
# weather report as a variable called mars_weather
# --------------------------------------------------------------------------
def marsWeather():
    browser = initBrowser()

    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)
    time.sleep(5)

    tweet_html = browser.html
    tweet_soup =BeautifulSoup(tweet_html, 'html.parser')
    time.sleep(5)

    weather_info_list = []

    for weather_info in tweet_soup.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        weather_info_list.append(weather_info.text.strip())

    for value in reversed(weather_info_list):
        if value[:3]=='Sol':
            mars_weather = value

    closeBrowser(browser)

    return mars_weather

# --------------------------------------------------------------------------
# Mars Facts - Visit the Mars Facts webpage here and use Pandas to scrape
# the table containing facts about the planet including Diameter, Mass, etc.
# --------------------------------------------------------------------------
def marsFacts():

    facts_url = 'https://space-facts.com/mars/'
    fact_list = pd.read_html(facts_url)
    time.sleep(5)
    facts_df = fact_list[0]
    facts_table = facts_df.to_html(header=False, index=False)

    return facts_table

# --------------------------------------------------------------------------
# Mars Hemisperes - Visit the USGS Astrogeology site to obtain
# high resolution images for each of Mars' hemispheres.
# --------------------------------------------------------------------------
def marsHemisphereImageURLs():

    browser = initBrowser()

    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)    
    time.sleep(5)       
    usgs_soup = BeautifulSoup(browser.html, 'html.parser')
    headers = []
    titles = usgs_soup.find_all('h3')  
    time.sleep(5)

    for title in titles: 
      headers.append(title.text)

    images = []
    count = 0
    for thumb in headers:
        browser.find_by_css('img.thumb')[count].click()
        images.append(browser.find_by_text('Sample')['href'])
        browser.back()
        count = count+1

    hemisphere_image_urls = []  #initialize empty list to collect titles
    counter = 0
    for item in images:
        hemisphere_image_urls.append({"title":headers[counter],"img_url":images[counter]})
        counter = counter+1
    closeBrowser(browser)
    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape())  #scrape method stores all scrape data as a json in terminal