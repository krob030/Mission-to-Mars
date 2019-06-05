from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import time
import pandas as pd
from selenium import webdriver

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    #Mars latest News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text
    news_title= news_title
    news_p= news_p
    #JPL Mars Space Images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    main_jpl= 'https://www.jpl.nasa.gov'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = soup.find('figure', class_='lede').find('a')['href']
    JPL= main_jpl+featured_image_url
    #Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find('p', class_='js-tweet-text').text
    mars_weather= mars_weather
    #Mars Facts
    url= 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_facts = soup.find('table', class_='tablepress tablepress-id-mars').text
    mars_table= pd.read_html(url)
    df = mars_table[0]
    df.columns = ['FACT', 'VALUE']
    #mars_table= df
    #mars_facts= mars_table
    mars_facts= df.to_html(classes="table table-striped")
    #Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_image_urls= []
    link= browser.find_by_css("a.product-item h3")
    for i in range(len(link)):
        base = {}
        browser.find_by_css("a.product-item h3")[i].click()
        url= browser.find_link_by_text("Sample").first
        base["title"] = browser.find_by_css("h2.title").text
        base["img_url"] = url["href"]
        hemisphere_image_urls.append(base)
        browser.back()
    hemisphere_image_urls =hemisphere_image_urls
    # Store data in a dictionary
    scrape_mars = {
        "news_title": news_title, 
        "news_p": news_p,
        "JPL": JPL,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return scrape_mars