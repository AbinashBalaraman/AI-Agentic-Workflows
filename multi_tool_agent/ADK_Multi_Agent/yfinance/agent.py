from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from .prompt import description
import warnings
import logging
import yfinance as yf
import warnings
import pprint as pp
from dotenv import load_dotenv
load_dotenv()


def fetch_stock_attribute(ticker: str, attribute: str) -> str:
    """
    Fetch a specific stock attribute and news and related data for a given ticker symbol or company name or organization name and return it as a string.

    Args:
        ticker (str): The stock ticker symbol.
        attribute (str): The attribute to fetch.

    Returns:
        str: The requested attribute's value as a string, or an error message if unavailable.
      Fetch stock data for a given ticker symbol and return it as a dictionary of strings.

    Args:
        ticker (str): The stock ticker symbol.
        attributes (list): List of attributes to fetch from yfinance.Ticker object. 
            If None, fetches a default set of attributes.

    Returns:
        dict: A dictionary where keys are attribute names and values are their string representations.

    Note:
        The `attributes` parameter should be one or more of the following keywords supported by yfinance.Ticker:
        
        - "info": General company information (dict)
        - "dividends": Dividend history (pandas.Series)
        - "splits": Stock split history (pandas.Series)
        - "actions": Dividends and splits combined (pandas.DataFrame)
        - "balance_sheet": Annual balance sheet (pandas.DataFrame)
        - "financials": Annual income statement (pandas.DataFrame)
        - "cashflow": Annual cash flow statement (pandas.DataFrame)
        - "quarterly_balance_sheet": Quarterly balance sheet (pandas.DataFrame)
        - "quarterly_financials": Quarterly income statement (pandas.DataFrame)
        - "quarterly_cashflow": Quarterly cash flow statement (pandas.DataFrame)
        - "sustainability": Sustainability data (pandas.DataFrame)
        - "calendar": Earnings calendar (pandas.DataFrame)
        - "earnings": Annual earnings (pandas.DataFrame)
        - "earnings_dates": Earnings announcement dates (pandas.DataFrame)
        - "analyst_price_targets": Analyst price targets (pandas.DataFrame)
        - "recommendations": Analyst recommendations (pandas.DataFrame)
        - "institutional_holders": Institutional holders (pandas.DataFrame)
        - "mutualfund_holders": Mutual fund holders (pandas.DataFrame)
        - "major_holders": Major holders (pandas.DataFrame)
        - "isin": International Securities Identification Number (str)
        - "shares": Shares data (dict)
        - "options": Option expiration dates (list)
        - "news": Latest news articles (list of dicts)

    Example:
        fetch_stock_data("AAPL", ["info", "dividends", "news"])

    This docstring helps AI understand which keywords to use when the user requests specific stock"""
    data = yf.Ticker(ticker)

    try:
        value = getattr(data, attribute)
        return str(value)
    except Exception as e:
        return f" Error fetching {attribute}: {e}"



def search_stock(company: str) -> str:
    """
    Search for a stock by company name and return the results as a string.

    Args:
        company (str): The company name to search for.
        max_results (int): Maximum number of search results to return.

    Returns:
        str: A string representation of the search results.
    """
    try:
        search = yf.Search(company)
        results = search.quotes
        return pp.pformat(results)
    except Exception as e:
        return f" Error searching for {company}: {e}"





root_agent= Agent(name="yfinace_agent",model=LiteLlm("openai/gpt-4o"),instruction=description,
description="""Fetch a specific stock attribute and news and related data for a given ticker symbol or company name or organization name """, tools=[search_stock,fetch_stock_attribute])