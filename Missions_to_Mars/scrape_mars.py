import os
import requests
from splinter import Browser
import pymongo
import pandas as pd
from bs4 import BeautifulSoup
import time


def init_browser():
    executable_path = {'executable_path':'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit mars.nasa.gov
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(2)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get the title of the first news
    the_title = soup.find('div', class='content_title')

    # Get the paragraph of the first news
    paragraphs = soup.find('div', class='article_teaser_body')

    # Get the URL for the featured URL
    photo_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(photo_url)

    # Set up for HTML scrapes
    p_html = browser.html
    soup_p = BeautifulSoup(p_html, 'html.parser')

    # Scrape URL for featured Image
    photos = soup_p.find('img', class_='thumb')['src']
    pre_url = 'http://www.jpl.nasa.gov'
    featured_image_url = pre_url + photos

    # Scrape for weather data
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url_weather)
    soup = BeautifulSoup(response.text, 'lxml')

    # find and scrape for weather data
    p_mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').getText()

    # Scrape for Mars Data
    mars_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_url)

    df_mars = tables[0]
    df_mars.columns =['Mars', 'Earth']

    html_table = df_mars.to_html()
    html_table.replace('\n', '')

    df_mars.to_html('index.html')

    mars_data = {
    'the_title': the_title,
    'paragraphs': paragraphs,
    'featured_image_url': featured_image_url,
    'mars_weather':p_mars_weather,
    'html_table': html_table
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data