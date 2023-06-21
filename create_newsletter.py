import openai
import environment as env
import summarize_reuters as s

def initalize_key():
    openai.api_key = env.OPENAI_API_KEY

def create_newsletter():
    initalize_key()
    #article_summaries = s.summarize_articles()

    article_summaries = []
    with open('output.txt', 'r') as file:
        for line in file:
            if len(line) > 30:
                article_summaries.append(line.strip())

    a, b = article_summaries[:len(article_summaries)//2], article_summaries[len(article_summaries)//2:]

    complete_response = []

    for lst in [a, b]:
        prompt = "Here are a collection of summaries of today's news. Summarize all these stories into one 400 word summary. Some news events may appear in more than one part of the collection of summaries. Write more about news events that appear more often. Make sure that the summary is objective and doesn't repeat the same event twice. Here are the summaries: "
        
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

    print(response)
    return response


create_newsletter()
