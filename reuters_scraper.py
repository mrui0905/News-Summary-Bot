from bs4 import BeautifulSoup
import requests

# Returns urls from Reuter's front page news
def retrieve_reuters(topic='world'):
    html = requests.get('https://www.reuters.com/' + topic + '/').text
    soup = BeautifulSoup(html, 'html.parser')

    articles =[]
    
    # Parse html for class 'a'
    for a_tag in soup.select('a[href*="/world"]'):
        link = a_tag['href']
        link = link[1:]
        articles.append(link)

    # Filter out general url's to get correct news articles
    articles = ['https://www.reuters.com/' + a for a in articles if len(a) > 20]

    return articles