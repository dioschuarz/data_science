from crewai import Agent
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.duck_search_tools import SearchTools
from tools.yfinance import FinancialsInfoTool


load_dotenv("../envs/invest.env")
llms = []
llms.append(ChatGroq(model="llama3-70b-8192",
                     temperature=0,
                     max_tokens=5000))
llms.append(ChatGoogleGenerativeAI(model="gemini-pro",
                                   temperature=0))
llms.append(ChatGroq(model="mixtral-8x7b-32768",
                     temperature=0,
                     max_tokens=5000))
llm = llms[0].with_fallbacks(llms[1:])


class StockAnalysisAgents():
  def financial_analyst(self):
    return Agent(
      role='The Best Financial Analyst',
      goal="""Impress all customers with your financial data 
      and market trends analysis""",
      backstory="""The most seasoned financial analyst with 
      lots of expertise in stock market analysis and investment
      strategies that is working for a super important customer.""",
      verbose=True,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        CalculatorTools.calculate,
        FinancialsInfoTool.search_stock_fundamentals,
        FinancialsInfoTool.specific_stock_fundamentals
      ],
      llm=llm
    )

  def research_analyst(self):
    return Agent(
      role='Staff Research Analyst',
      goal="""Being the best at gather, interpret data and amaze
      your customer with it""",
      backstory="""Known as the BEST research analyst, you're
      skilled in sifting through news, company announcements, 
      and market sentiments. Now you're working on a super 
      important customer""",
      verbose=True,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        FinancialsInfoTool.search_stock_fundamentals,
        FinancialsInfoTool.specific_stock_fundamentals
      ],
      llm=llm
  )

  def investment_advisor(self):
    return Agent(
      role='Private Investment Advisor',
      goal="""Impress your customers with full analyses over stocks
      and completer investment recommendations""",
      backstory="""You're the most experienced investment advisor
      and you combine various analytical insights to formulate
      strategic investment advice. You are now working for
      a super important customer you need to impress.""",
      verbose=True,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        CalculatorTools.calculate
      ],
      llm=llm
    )