from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    listings = {}

    # Mars facts
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

  
    news_title = soup.find('div', class_='content_title').text

    news_p = soup.find('div', class_='article_teaser_body').text

    listings["news_title"] = soup.find('div', class_='content_title').get_text()
    listings["news_p"] = soup.find('div', class_='article_teaser_body').get_text()

    # Space Images
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find('div', class_= 'fancybox-inner')

    img = results.find('img')
    link = img['src']

    listings["featured_image_url"] = f'https://spaceimages-mars.com/{link}'

    # Mars Table

    url = 'https://galaxyfacts-mars.com'

    # read in tables, and print them
    tables = pd.read_html(url)

    df = tables[1]

    df.to_html('marsfact_table.html', header = False, index = False, classes= 'table')

    # body = [body.text for body in table.find('tbody')]
    # listings["results"] = [{body[i]: cell for i, cell in enumerate(row.find_all('td'))}
    #            for row in table.find_all('tr')]


# In[ ]:


# Saving desired table to html and not including the header or index

    # import bs4 and create your 'soup' object

    # table = soup.find('table')

    # https://stackoverflow.com/questions/11901846/beautifulsoup-a-dictionary-from-an-html-table
    # headers = [header.text for header in table.find_all('th')]
    # results = [{headers[i]: cell for i, cell in enumerate(row.find_all('td'))}
    #            for row in table.find_all('tr')]

    # table = tables[1]

    # body = [body.text for body in table.find('tbody')]
    # listings["results"] = [{body[i]: cell for i, cell in enumerate(row.find_all('td'))}
    #            for row in table.find_all('tr')]

    # Mars Hemispheres 

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Scrape html and find all div, class descriptions
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_='description')

    title_list = []

    # Looping through results to find the titles, split, and append to list
    for result in results:
        title_txt = result.find('h3').text
        title = title_txt.split('Enhanced')[0]
        title_list.append(title)


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

                listings['img_title'] = value
                listings['img_url'] = img_url
                
                # Add one to index to move on next item
                index+=1

    # Quit the browser
    browser.quit()

    return listings

print("Data Uploaded!")