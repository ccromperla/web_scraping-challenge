# Imports
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt 

# Function to scrape all necessary data
def scrape_all(): 

    #Setting up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Grabbing info from the news page
    news_title, news_p = scrape_news(browser)

    marsData = {
        "newsTitle" : news_title,
        "newsParagraph" : news_p,
        "featuredImage" : scrape_featimg(browser),
        "facts" : scrape_facts(browser),
        "hemispheres" : scrape_hemispheres(browser),
        "lastUpdated" : dt.datetime.now()
    }

    # Quit the browser
    browser.quit()

    return marsData


#Function to scrape through Red Planet Science
def scrape_news(browser):
    
    # Go to url
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading news page 
    browser.is_element_present_by_css('div.list_text', wait_time = 1)

    # HTML Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    slide_elem = soup.select_one('div.list_text')

    # Grabbing News title 
    news_title = slide_elem.find('div', class_='content_title').get_text()
    
    # Grabbing news paragraph
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    return news_title, news_p

def scrape_featimg(browser):
    
    # Visit new site to find image jpg. for feature image
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Use splint to click on FULL IMAGE button
    browser.links.find_by_partial_text('FULL IMAGE').click()

    # Scrape html
    html = browser.html
    soup = bs(html, 'html.parser')

    # Store class with fancybox-inner in results
    results = soup.find('div', class_= 'fancybox-inner')
    
    # Find image tag and index into img to find src
    img = results.find('img')
    link = img['src']

    # Get link to image and print it
    featured_image_url = f'https://spaceimages-mars.com/{link}'
    
    return featured_image_url

def scrape_facts(browser):
    # URL to visit
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find Mars facts locations
    facts_loc = soup.find('div', class_= 'sidebar')
    facts_table = facts_loc.find('table', class_= 'table table-striped')

    # Create and empty string
    facts = ""

    # Add text to empty string using return 
    facts += str(facts_table)

    return facts

def scrape_hemispheres(browser):
    # Base url
    url = 'https://marshemispheres.com/'
    browser.visit(url) 

    # Create a list to hold image urls and titles
    hemisphere_image_urls = []

    # Set up loop for each page
    for i in range(4):
        
        # Dictionary
        hemisphereInfo = {}
         
        # Find elements of each loop to avoid a stale elemect exception
        browser.find_by_css('a.product-item img')[i].click()

        # Next find the Sample image anchor tag and extract href 
        sample = browser.links.find_by_text('Sample').first
        hemisphereInfo['img_url'] = sample['href']

        # Get hemisphere title
        hemisphereInfo['title'] = browser.find_by_css('h2.title').text

        # Append hemisphere pbj to list
        hemisphere_image_urls.append(hemisphereInfo)

        # Navigate backwards
        browser.back()

    # Return hemisphere urls with titles 
    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape_all())