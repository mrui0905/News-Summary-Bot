from bs4 import BeautifulSoup
import requests
import reuters_scraper as rs
import environment as env
import openai

def initalize_key():
    openai.api_key = env.OPENAI_API_KEY

def summarize_articles():
    initalize_key()
    article_summaries = []

    articles = rs.retrieve_reuters()

    for article in articles[:40]:
        html = requests.get(article).text
        soup = BeautifulSoup(html, 'html.parser')

        article_text = ''
        try:
            soup.find('p', class_=lambda x: x.startswith('text__'))
        except:
            continue

        for p in soup.find_all('p', class_=lambda x: x.startswith('text__')):
            article_text += p.text


        prompt = "Here is the text of an article which also includes photo captions, advertisements, and disclaimers. Ignore all of the above and summarize ONLY the article text in roughly 50 words."
        
        response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt+article_text,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
        )

        summary = response.choices[0].text.strip()
        article_summaries.append(summary)
    article_summaries = [a for a in article_summaries if len(a) > 30]
    return article_summaries
    
def save_list_to_file(lst, filename):
    with open(filename, 'w') as file:
        for item in lst:
            file.write(item + '\n')

#save_list_to_file(summarize_articles(), 'output.txt')

        



