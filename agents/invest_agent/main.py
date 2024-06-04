from crewai import Crew
from dotenv import load_dotenv
from textwrap import dedent


load_dotenv("../envs/invest.env")

class FinancialCrew:
  def __init__(self, company):
    self.company = company

  def run(self):
    from stock_analysis_agents import StockAnalysisAgents
    from stock_analysis_tasks import StockAnalysisTasks

    agents = StockAnalysisAgents()
    tasks = StockAnalysisTasks()

    research_analyst_agent = agents.research_analyst()
    financial_analyst_agent = agents.financial_analyst()
    investment_advisor_agent = agents.investment_advisor()

    research_task = tasks.research(research_analyst_agent, self.company)
    financial_task = tasks.financial_analysis(financial_analyst_agent, self.company)
    #filings_task = tasks.filings_analysis(financial_analyst_agent, self.company)
    strategy_task = tasks.strategy_analysis(financial_analyst_agent, self.company)
    recommend_task = tasks.recommend(investment_advisor_agent, self.company)

    crew = Crew(
      agents=[
        research_analyst_agent,
        financial_analyst_agent,
        investment_advisor_agent
      ],
      tasks=[
        research_task,
        financial_task,
        #filings_task,
        strategy_task,
        recommend_task
      ],
      verbose=True
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
  print("## Welcome to Financial Analysis Crew")
  print('-------------------------------')
  company = input(
    dedent("""
      What is the company you want to analyze?
    """))
  
  financial_crew = FinancialCrew(company)
  result = financial_crew.run()
  print("\n\n########################")
  print("## Here is the Report")
  print("########################\n")
  print(result)
