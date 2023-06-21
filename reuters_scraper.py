from bs4 import BeautifulSoup
import requests

'''
r = requests.get('https://www.reuters.com/world/')
soup = bs4.BeautifulSoup(r.text, 'html.parser')

articles = soup.findAll(class_= "media-story-card__body__3tRWy")

links = []
for article in articles:
    tmp = article.find('a')
    print(tmp)
    links.append(tmp['href'])

print(links)
'''

# Returns urls from Reuter's front page news
def retrieve_reuters():
    html = requests.get('https://www.reuters.com/world/').text
    soup = BeautifulSoup(html, 'html.parser')

    articles =[]

    for a_tag in soup.select('a[href*="/world"]'):
        link = a_tag['href']
        link = link[1:]
        articles.append(link)

    articles = ['https://www.reuters.com/' + a for a in articles if len(a) > 20]

    return articles
