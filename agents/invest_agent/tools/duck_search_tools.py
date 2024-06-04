from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
import re


class SearchTools():
  @tool("Search the internet")
  def search_internet(query):
    """Useful to search the internet 
    about a a given topic and return relevant results"""
    top_result_to_return = 4
    wrapper = DuckDuckGoSearchAPIWrapper(max_results=top_result_to_return)
    search = DuckDuckGoSearchResults(api_wrapper=wrapper,
                                     source="search",
                                     num_results=top_result_to_return)
    news = search.run(query)
    pattern = r'\[([^\]]+)\]'
    pattern_news = r"snippet: (.*?), title: (.*?), link: (.*?)$"
    my_news_list = re.findall(pattern, news)
    string = []
    for result in my_news_list:
        match = re.match(pattern_news, result)
        if match:
            snippet, title, link = match.groups()
            result = {"snippet": snippet, "title": title, "link": link}
            try:
                string.append('\n'.join([
                    f"Title: {result['title']}", f"Link: {result['link']}",
                    f"Snippet: {result['snippet']}", "\n-----------------"
                    ]))
            except KeyError:
              next

    return '\n'.join(string)

  @tool("Search news on the internet")
  def search_news(query):
    """Useful to search news about a company, stock or any other
    topic and return relevant results"""""
    top_result_to_return = 4
    wrapper = DuckDuckGoSearchAPIWrapper(max_results=top_result_to_return)
    search = DuckDuckGoSearchResults(api_wrapper=wrapper,
                                     source="news",
                                     num_results=top_result_to_return)
    news = search.run(query)
    pattern = r'\[([^\]]+)\]'
    pattern_news = r"snippet: (.*?), title: (.*?), link: (.*?)$"
    my_news_list = re.findall(pattern, news)
    string = []
    for result in my_news_list:
        match = re.match(pattern_news, result)
        if match:
            snippet, title, link = match.groups()
            result = {"snippet": snippet, "title": title, "link": link}
            try:
                string.append('\n'.join([
                    f"Title: {result['title']}", f"Link: {result['link']}",
                    f"Snippet: {result['snippet']}", "\n-----------------"
                    ]))
            except KeyError:
              next

    return '\n'.join(string)
