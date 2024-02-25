import os
from dotenv import find_dotenv, load_dotenv
import requests
import json
from langchain import OpenAI,  LLMChain, PromptTemplate
import openai

load_dotenv(find_dotenv())
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# 1) get relevant google search results using SERP API
def search(query):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    })
    headers = {
        'X-API-KEY': SERPAPI_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST",url, headers=headers, data=payload)
    response_data = response.json()

    print("search results: ", response_data)
    return response_data


search("how do self-driving cars function?")

# 2) get LLM to choose the best ones from the search results

def find_best_article_urls(response_data, query):

    response_str = json.dumps(response_data)

    llm = OpenAI(model_name="gpt-3.5-turbo", temparature=0.7)
    template = """
    You are a world class journalist & researcher, you are extremely good at finding the most relevant articles for any given topic.
    {response_str}
    Above is the list of search results for the query {query}
    Please choose the best 3 articles from the list, return ONLY an array of the URLS, do not return anything else.
    """

    prompt_template = PromptTemplate(input_variables=["response_str", "query"], template=template)

    article_picker_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)

    urls = article_picker_chain.predict(response_str=response_str, query=query)
