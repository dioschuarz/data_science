from langchain_core.tools import tool
import yfinance as yf

class FinancialsInfoTool():
  @tool("Financials General Information Tool")
  def search_stock_fundamentals(data):
    """
    Provide relevant information for fundamental stock analysis 
    that this library can offer, including details about the 
    Trailling EPS, Foward EPS, Book Value, Dividend Yield, Beta,
    EBITDA, Debts, Revenue per Share. Return on Assets and Margins.
		For example, {'data': 'AAPL'}.
    """
    ticker = yf.Ticker(data)
    if len(ticker.info) == 0:
      return "Sorry, I couldn't find any filling for this stock, check if the ticker is correct."
    answer = ticker.info
    return answer
  @tool("Financials Specific Information Tool")
  def specific_stock_fundamentals(data, field):
    """
    Provide one specific information from fundamental stock analysis 
    that this library can offer, including details about the 
    Trailling EPS, Foward EPS, Book Value, Dividend Yield, Beta,
    EBITDA, Debts, Revenue per Share. Return on Assets and Margins.
		For example, {'data': 'AAPL', 'field': 'trailingEps'}.
    """
    ticker = yf.Ticker(data)
    if len(ticker.info) == 0:
      return "Sorry, I couldn't find any filling for this stock, check if the ticker is correct."
    answer = ticker.info
    try:
      return answer[field]
    except:
      return f"This stock does not has the field {field}, please try another one from the given list {answer.keys()}."