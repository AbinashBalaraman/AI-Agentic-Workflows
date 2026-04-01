import os
import yfinance as yf
from langchain.tools import tool
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langgraph.prebuilt import create_react_agent
import google.generativeai as genai
from langchain.chat_models import init_chat_model

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from dotenv import load_dotenv
load_dotenv()

@tool
def get_stock_info(a: str) -> str:
    """Get general information about the given company"""
    ticker = yf.Ticker(a)
    info = ticker.info
    return str(info) if info else "No info data available"
@tool
def get_stock_dividends(a: str) -> str:
    """Get dividend history of the given company"""
    ticker = yf.Ticker(a)
    dividends = ticker.dividends
    return dividends.to_string() if dividends is not None else "No dividends data available"
@tool
def get_stock_splits(a: str) -> str:
    """Get stock split history of the given company"""
    ticker = yf.Ticker(a)
    splits = ticker.splits
    return splits.to_string() if splits is not None else "No splits data available"
@tool
def get_stock_actions(a: str) -> str:
    """Get actions (dividends and splits) of the given company"""
    ticker = yf.Ticker(a)
    actions = ticker.actions
    return actions.to_string() if actions is not None else "No actions data available"
@tool
def get_stock_balance_sheet(a: str) -> str:
    """Get annual balance sheet of the given company"""
    ticker = yf.Ticker(a)
    balance_sheet = ticker.balance_sheet
    return balance_sheet.to_string() if balance_sheet is not None else "No balance sheet data available"
@tool
def get_stock_financials(a: str) -> str:
    """Get annual income statement (financials) of the given company"""
    ticker = yf.Ticker(a)
    financials = ticker.financials
    return financials.to_string() if financials is not None else "No financials data available"
@tool
def get_stock_cashflow(a: str) -> str:
    """Get annual cash flow statement of the given company"""
    ticker = yf.Ticker(a)
    cashflow = ticker.cashflow
    return cashflow.to_string() if cashflow is not None else "No cash flow data available"
@tool
def get_stock_quarterly_balance_sheet(a: str) -> str:
    """Get quarterly balance sheet of the given company"""
    ticker = yf.Ticker(a)
    balance_sheet = ticker.quarterly_balance_sheet
    return balance_sheet.to_string() if balance_sheet is not None else "No quarterly balance sheet data available"
@tool
def get_stock_quarterly_financials(a: str) -> str:
    """Get quarterly income statement of the given company"""
    ticker = yf.Ticker(a)
    financials = ticker.quarterly_financials
    return financials.to_string() if financials is not None else "No quarterly financials data available"
@tool
def get_stock_quarterly_cashflow(a: str) -> str:
    """Get quarterly cash flow statement of the given company"""
    ticker = yf.Ticker(a)
    cashflow = ticker.quarterly_cashflow
    return cashflow.to_string() if cashflow is not None else "No quarterly cash flow data available"
@tool
def get_stock_sustainability(a: str) -> str:
    """Get sustainability data of the given company"""
    ticker = yf.Ticker(a)
    sustainability = ticker.sustainability
    return str(sustainability) if sustainability is not None else "No sustainability data available"
@tool
def get_stock_calendar(a: str) -> str:
    """Get earnings calendar of the given company"""
    ticker = yf.Ticker(a)
    calendar = ticker.calendar
    return str(calendar) if calendar is not None else "No calendar data available"
@tool
def get_stock_earnings(a: str) -> str:
    """Get earnings data of the given company"""
    ticker = yf.Ticker(a)
    earnings = ticker.earnings
    return earnings.to_string() if earnings is not None else "No earnings data available"
@tool
def get_stock_earnings_dates(a: str) -> str:
    """Get earnings announcement dates of the given company"""
    ticker = yf.Ticker(a)
    earnings_dates = ticker.earnings_dates
    # print(earnings_dates)
    return earnings_dates.to_string() if earnings_dates is not None else "No earnings dates data available"
@tool
def get_stock_analyst_price_targets(a: str) -> str:
    """Get analyst price targets for the given company"""
    ticker = yf.Ticker(a)
    price_targets = ticker.analyst_price_targets
    # print(price_targets)
    return str(price_targets) if price_targets is not None else "No analyst price targets data available"
@tool
def get_stock_recommendations(a: str) -> str:
    """Get analyst recommendations for the given company"""
    ticker = yf.Ticker(a)
    recommendations = ticker.recommendations
    # print(recommendations)
    return str(recommendations) if recommendations is not None else "No recommendations data available"
@tool
def get_stock_institutional_holders(a: str) -> str:
    """Get institutional holders of the given company"""
    ticker = yf.Ticker(a)
    holders = ticker.institutional_holders
    # print(holders)
    return holders.to_string() if holders is not None else "No institutional holders data available"
@tool
def get_stock_mutualfund_holders(a: str) -> str:
    """Get mutual fund holders of the given company"""
    ticker = yf.Ticker(a)
    holders = ticker.mutualfund_holders
    # print(holders)
    return holders.to_string() if holders is not None else "No mutual fund holders data available"
@tool
def get_stock_major_holders(a: str) -> str:
    """Get major holders of the given company"""
    ticker = yf.Ticker(a)
    holders = ticker.major_holders
    # print(holders)
    return holders.to_string() if holders is not None else "No major holders data available"
@tool
def get_stock_isin(a: str) -> str:
    """Get ISIN of the given company"""
    ticker = yf.Ticker(a)
    isin = ticker.isin
    # print(isin)
    return isin if isin is not None else "No ISIN data available"
@tool
def get_stock_shares(a: str) -> str:
    """Get shares data of the given company"""
    ticker = yf.Ticker(a)
    shares = ticker.shares
    # print(shares)
    return str(shares) if shares is not None else "No shares data available"
@tool
def get_stock_options(a: str) -> str:
    """Get option expiration dates of the given company"""
    ticker = yf.Ticker(a)
    options = ticker.options
    print(options)
    return str(options) if options else "No options data available"
@tool
def stock_search(query: str) -> str:
    """Get search results for a company name or ticker from Yahoo Finance"""
    try:
        search = yf.Search(query, max_results=10)
        quotes = search.quotes
        if not quotes:
            return "No search results found"
        result = "Search Results:\n"
        for quote in quotes:
            result += f"Symbol: {quote.get('symbol', 'N/A')}, "
            result += f"Name: {quote.get('shortname', 'N/A')}, "
            result += f"Exchange: {quote.get('exchDisp', 'N/A')}\n"
        return result
    except Exception as e:
        return f"Error fetching search results: {str(e)}"
@tool
def get_stock_news(a:str) -> str:
    """Get full news about given company and always give all the news you can find from the tool dont give part of the news  and dont left out any part of the each news eg. links of the source """
    ticker = yf.Ticker(a)
    info = ticker.news
    return str(info)
 
model = init_chat_model(model='gpt-4.1-mini',model_provider="openai")
tools = [stock_search,get_stock_news]#,get_stock_info,get_stock_analyst_price_targets,get_stock_actions,get_stock_balance_sheet,get_stock_calendar,get_stock_dividends,get_stock_cashflow,get_stock_earnings,get_stock_financials,get_stock_sustainability,get_stock_isin,get_stock_major_holders,get_stock_quarterly_cashflow,get_stock_mutualfund_holders,get_stock_shares,get_stock_splits,get_stock_quarterly_balance_sheet,get_stock_quarterly_financials,get_stock_earnings_dates,get_stock_recommendations,get_stock_institutional_holders,get_stock_options]
agent=create_react_agent(model,tools,debug=True)

system_prompt ="""Use available tools for get details about given company name or stock market ticker and Before using any tool make sure the stock market ticker is correct even if the user given the company name or ticker with typo pass correct ticker to the tool like "AAPL" for company apple also use stock search tool for getting ticker for indian market or us  skip the image content give as much text as possible"""
chat_history=[]


while True:
    input_text= input("Enter your query: ")
    if input_text.strip():
        if input_text.lower() in ["exit", "quit"]:
            # print("Goodbye!")
            break
        chat_history.append(('system', system_prompt))
        messages = [('user',input_text)]+chat_history
        events = agent.stream({"messages": messages
        },
        stream_mode="values",)
        for event in events:
            reply = event["messages"][-1].content
            # print("Assistant:", reply)
            chat_history.append(('assistant', reply))

def api_call(req):


