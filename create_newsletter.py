import openai
from dotenv import load_dotenv
import os
import summarize_reuters as s

# Initalize API Keys
def initalize_key():
    load_dotenv()

    openai.api_key = os.getenv('OPENAI_API_KEY')

def create_newsletter(topic):
    initalize_key() # Ensure API is validated
    article_summaries = s.summarize_articles(topic) # Retrieve article url's

    # Split article summaries into 2 equally long lists
    a, b = article_summaries[:len(article_summaries)//2], article_summaries[len(article_summaries)//2:]

    complete_response = []

    # Summarize each group of summaries
    for lst in [a, b]:
        prompt = "Here are a collection of summaries. Summarize these summary into one summary of approximately 400 words. Some news events may appear in more than one part of the collection of summaries. Write more about news events that appear more often. Make sure that the summary is objective and doesn't repeat the same event twice. Here are the summaries: "
        
        response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt+' '.join(lst),
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
        )

        response = response.choices[0].text.strip()
        complete_response.append(response)

    # Combined two summaries into one final summary 
    prompt = "Here are a collection of summaries. Summarize these summary into one summary of approximately 400 words. Some news events may appear in more than one part of the collection of summaries. Write more about news events that appear more often. Make sure that the summary is objective and doesn't repeat the same event twice. Here are the summaries: "
    
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt+' '.join(complete_response),
    max_tokens=1000,
    n=1,
    stop=None,
    temperature=0.7,
    )

    response = response.choices[0].text.strip()

    return response



