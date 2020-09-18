from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd  
import time
import pymongo
import re

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
    

def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    title_header = soup.find('div', class_='list_text')
    news_title = title_header.find('div', class_="content_title").text
    news_p = title_header.find('div', class_="article_teaser_body").text

    mars_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_url)

    #Find full size image after click Full image button
    browser.find_link_by_partial_text("FULL IMAGE").click()
    browser.find_link_by_partial_text("more info").click()

    html = browser.html
    soup = bs(html, 'html.parser')

        #Find image
    img_url_relative_path = soup.find('figure', class_='lede').a['href']

    #use base url to create absolute url
    featured_img_url = f"https://www.jpl.nasa.gov{img_url_relative_path}"


    table_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(table_url)
    mars_df = tables[2]

    html_table = mars_df.to_html()

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    hemisphere_image_urls = []

    baseimg_url="https://astrogeology.usgs.gov/"
    # Soup object
    hemispheres = soup.find_all('div', class_='item')
    # Loop to get each title & url
    for hemi in hemispheres:
        title = hemi.find('h3').text
        link = 'https://astrogeology.usgs.gov/' + hemi.find('a')['href']
        browser.visit(link)
        img_html = browser.html
        img_soup = bs(img_html, "html.parser")
        imgs_url = img_soup.find("img", class_="wide-image")["src"]
        image_url = baseimg_url+imgs_url
        hemisphere_image_urls.append({"title": title, "img_url": image_url})
        
    browser.quit()

   # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_img_url,
        "mars_facts": html_table,
        "hemispheres": hemisphere_image_urls
    }
    # Return results
    return mars_data
