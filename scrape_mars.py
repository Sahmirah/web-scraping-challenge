# Import Libraries
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # List the URL we want to scrape
    url = 'https://redplanetscience.com/'

    # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url)

    # Let it sleep for 1 second
    time.sleep(1)

    # Return all the HTML on our page
    html = browser.html

    # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
    soup = BeautifulSoup(html, "html.parser")

    # Find the latest news info
    title_news = soup.find('div', class_='content_title').text
    body_news = soup.find('div', class_='article_teaser_body').text
    
    # Place JPL Mars image
    jpl_img = 'https://spaceimages-mars.com/'
    browser.visit(jpl_img)
    html = browser.html

    # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
    soup = BeautifulSoup(html, "html.parser")

    image_src=soup.find_all('img', class_='headerimage fade-in')
 
    for element in image_src:
        print (element['src'])

    feat_img = jpl_img+element['src']

    #define mars info
    facts_url = 'https://galaxyfacts-mars.com/'
    all_tables = pd.read_html(facts_url)
    all_tables[1]
    mars_tables = all_tables[1].to_html(index=False)

    # define mars hemisphere data
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    html = browser.html

    # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
    soup = BeautifulSoup(html, "html.parser")

    # get the elements 
    hem_location = soup.find('div',class_='collapsible results')
    hem_items = hem_location.find_all('div',class_='item')

    # setup dictionary list to pick up each title and source
    hemi_img_url = []

    # Use a for loop with error handling to find each pic title and src
    for item in hem_items:
        try:
                hemi = item.find('div',class_='description')
                name = hemi.h3.text
                hem_button = hemi.a['href']
                browser.visit(hemi_img_url+ hem_button)
                html = browser.html
                soup = BeautifulSoup(html,'html.parser')
                img_find = soup.find('img',class_='wide-image')['src']
                dictionary ={'title':name, 'image_url':hemi_img_url+img_find}
                hemi_img_url.append(dictionary)
        except Exception as error:
             print(f"Error occurred: {error}")
                

 

    mars_data = {
          'news_title':title_news,
          'news_para':body_news,
          'featured_image_url':feat_img,
          'mars_specs': mars_tables,
          'hemispheres': hemi_img_url
    }

    print(mars_data)
    browser.quit()
    return mars_data
 
    