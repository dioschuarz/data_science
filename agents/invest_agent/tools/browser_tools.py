import os

import requests
from crewai import Agent, Task
from langchain_core.tools import tool
from unstructured.partition.html import partition_html


class BrowserTools():

  @tool("Scrape website content")
  def scrape_and_summarize_website(url):
    """Useful to scrape and summarize a website content"""
    website = url["url"]
    api = f"https://api.scrapingdog.com/scrape?api_key={os.environ['SCRAPPING_DOG_API_KEY']}"
    url = f"&url={website}&dynamic=false"
    uri = api + url
    response = requests.request("GET", uri)
    elements = partition_html(text=response.text)
    content = "\n\n".join([str(el) for el in elements])
    content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
    summaries = []
    for chunk in content:
      agent = Agent(
          role='Principal Researcher',
          goal=
          'Do amazing research and summaries based on the content you are working with',
          backstory=
          "You're a Principal Researcher at a big company and you need to do research about a given topic.",
          allow_delegation=False)
      task = Task(
          agent=agent,
          description=
          f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
      )
      summary = task.execute()
      summaries.append(summary)
    return "\n\n".join(summaries)
