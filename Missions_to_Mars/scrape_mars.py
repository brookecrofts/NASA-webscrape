from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt   
import time
import re


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape_info():
    news_title, news_p = mars_news(browser)
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image,
        "mars_facts": mars_facts,
        "hemispheres": hemispheres

    }
    # Close the browser after scraping
    browser.quit()
    # Return results
    return mars_data

def mars_news(browser):
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    try:
        news = soup.find('div', class_="content_title").text
        news_title = news.strip('\n')
        news_2 = soup.find('div', class_="rollover_description_inner").text
        news_p = news_2.strip('\n')
        # "div", class_="article_teaser_body").get
    except AttributeError:
        return None, None
    
    return news_title, news_p

def featured_image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    #Find full size image after click Full image button
    full_image = browser.find_by_id("full_image")
    full_image.click()

    html = browser.html
    img_soup = BeautifulSoup(html, "html.parser")

    img = img_soup.select_one("figure.lede a img")

    try: 
        img_url_relative_path = img.get("src")

    except AttributeError:
        return None

    #use base url to create absolute url
    featured_img_url = f"https://www.jpl.nasa.gov{img_url_relative_path}"

    return featured_img_url

def mars_facts:
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    try:
    nasa_df = tables[2]

    except AttributeError:
        return None

    return nasa_df

def hemispheres(browser):

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(url)

    hemisphere_image_urls = []
    for i in range(4):

        browser.find_by_css("a.product-item h3")[i].click()

        hemi_data = scrape_hemisphere(browser.html)

        #Append to the list
        hemisphere_image_urls.append(hemi_data)

        #Go back to previous page to get next one
        browser.back()

    return hemisphere_image_urls


    # # BONUS: Find the src for the sloth image
    # relative_image_path = soup.find_all('img')[2]["src"]
    # sloth_img = url + relative_image_path

