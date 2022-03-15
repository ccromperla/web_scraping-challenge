#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager


# In[ ]:


# Setup splinter

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ## NASA MARS NEWS

# In[ ]:


# URL to visit
url = 'https://redplanetscience.com/'
browser.visit(url)


# In[ ]:


# Scrape the latest News Title & Paragraph Text 
html = browser.html
soup = bs(html, 'html.parser')


# In[ ]:


# Find news_title and news_p

news_title = soup.find('div', class_='content_title').text

news_p = soup.find('div', class_='article_teaser_body').text

print(f"Title: {news_title}")
print(f"Article: {news_p}")


# ## JPL Mars Space Image

# In[ ]:


# Visit new site to find image jpg. for feature image
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[ ]:


# Use splint to click on FULL IMAGE button
browser.links.find_by_partial_text('FULL IMAGE').click()


# In[ ]:


# Scrape html
html = browser.html
soup = bs(html, 'html.parser')


# In[ ]:


# Store class with fancybox-inner in results
results = soup.find('div', class_= 'fancybox-inner')


# In[ ]:


# find image tag and index into img to find src
img = results.find('img')
link = img['src']


# In[ ]:


# get link to image and print it
featured_image_url = f'https://spaceimages-mars.com/{link}'
print(featured_image_url)


# ## Mars Facts

# In[ ]:


# Use pandas to scrape table from url
url = 'https://galaxyfacts-mars.com'

# read in tables, and print them
tables = pd.read_html(url)
tables


# In[ ]:


# Index into list to see the tables we have: Mars & Earth Comparison
tables[0]


# In[ ]:


# Index into second list item where we have Mars facts only (I prefer this one)
tables[1]


# In[ ]:


# Save desired table to Variable df 
df = tables[1]
df


# In[ ]:


# Saving desired table to html and not including the header or index
df.to_html('marsfact_table.html', header = False, index = False, classes= 'table')


# ## Mars Hemispheres

# In[ ]:


# Visit new site to find image jpg. for Mars Hemisphere
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[ ]:


# Scrape html and find all div, class descriptions
html = browser.html
soup = bs(html, 'html.parser')

results = soup.find_all('div', class_='description')


# In[ ]:


# Empty list to store titles
title_list = []

# Looping through results to find the titles, split, and append to list
for result in results:
    title_txt = result.find('h3').text
    title = title_txt.split('Enhanced')[0]
    title_list.append(title)


# In[ ]:


# List that will become a list of dictionaries
hemisphere_image_urls = []

# Using enumerate to go into titles list
for index, value in enumerate(title_list):
       
    # If statement to break out of loop when index is at 4 
    if index == 4:
        break
      
    # If the loop isn't ==4 then... get the value(title) to click into page
    else:
        url = 'https://marshemispheres.com/'
        browser.visit(url)  
        browser.links.find_by_partial_text(value).click()
        
        # Scrape html and grab download div
        html = browser.html
        soup = bs(html, 'html.parser')
        results = soup.find_all('div', class_='downloads')

        # Loop through the results to get image link in .jpg
        for result in results:
            u_list = result.find('ul')
            l_list = u_list.find('li')
            article = l_list.find('a')
            link = article['href']
            img_url = f'https://marshemispheres.com/{link}'

            # Store value and img_url as a dict
            img_dict = {
                'title' : value,
                'img_url' : img_url
            }

            # Append dictionary into hemisphere_image_urls list
            hemisphere_image_urls.append(img_dict)
            
            # Add one to index to move on next item
            index+=1

# Print list of dictionary
print(hemisphere_image_urls)


# In[ ]:


# Quit browser once scraping is complete
browser.quit()

