import yfinance as yf
import pandas as pd
import os
import warnings
from rich import print
def test1_yfinance(ticker: str):
    warnings.simplefilter("ignore", DeprecationWarning)

    data = yf.Ticker(ticker)
    path = os.path.join(os.path.curdir, 'Exported')
    os.makedirs(path, exist_ok=True)

    # ✅ Valid attributes in yfinance's Ticker object
    valid_attributes = [
        "calendar"
    ]

    for attr in valid_attributes:
        try:
            value = getattr(data, attr)
            print(data)
        #     if isinstance(value, pd.DataFrame):
        #         # ⏱️ Remove timezone awareness if necessary
        #         if isinstance(value.index, pd.DatetimeIndex) and value.index.tzinfo is not None:
        #             value.index = value.index.tz_localize(None)
        #         value.to_excel(os.path.join(path, f"{ticker}_{attr}.xlsx"))
        #     elif isinstance(value, dict):
        #         pd.DataFrame([value]).to_excel(os.path.join(path, f"{ticker}_{attr}.xlsx"))
        except Exception as e:
            print(f"⚠️ Error processing {attr}: {e}")

    # 🔔 Special case for dividends
    # try:
    #     hist = data.dividends
    #     if isinstance(hist.index, pd.DatetimeIndex):
    #         hist.index = hist.index.tz_localize(None)
    #     hist.to_excel(os.path.join(path, f"{ticker}_dividends.xlsx"))
    # except Exception as e:
    #     print(f"⚠️ Error exporting dividends: {e}")

# 🧪 Example usage
#test1_yfinance("MSFT")
# import yfinance as yf
# import pandas as pd
# import os
import pprint as pp
import yaml

# # data = yf.Ticker('TATAMOTORS.NS')
# # hist = data.history(period = '1mo')
# # print(hist)

# import yfinance as yf
# import os
# import pandas as pd

def tesqt_yfinance(ticker: str):
    data = yf.Ticker(ticker)
    path = os.path.join(os.path.curdir, 'Exported')
    os.makedirs(path, exist_ok=True)

    attributes = [
        "earnings", "earnings_dates", "earnings_estimates", "earnings_history",
        "eps_revisions", "eps_trend", "fast_info", "financials", "funds_data",
        "growth_estimates", "income_stmt", "incomestmt", "info", "insider_purchases",
        "insider_roster_holders", "insider_transactions", "institutional_holders",
        "isin", "major_holders", "mutualfund_holders", "news", "options",
        "quarterly_balance_sheet", "quarterly_balancesheet", "quarterly_cash_flow",
        "quarterly_cashflow", "quarterly_earnings", "quarterly_financials",
        "quarterly_income_stmt", "quarterly_incomestmt", "recommendations",
        "recommendations_summary", "revenue_estimates", "sec_filings", "shares",
        "splits", "sustainability", "ttm_cash_flow", "ttm_cashflow", "ttm_financials",
        "ttm_income_stmt", "ttm_incomestmt", "upgrades_downgrades"
    ]

    for attr in attributes:
        try:
            value = getattr(data, attr)
            if hasattr(value, "to_excel"):
                value.to_excel(os.path.join(path, f"{ticker}_{attr}.xlsx"))
            elif isinstance(value, pd.DataFrame):
                value.to_excel(os.path.join(path, f"{ticker}_{attr}.xlsx"))
            elif isinstance(value, dict):
                df = pd.DataFrame([value])
                df.to_excel(os.path.join(path, f"{ticker}_{attr}.xlsx"))
        except Exception as e:
            print(f"Error processing {attr}: {e}")

    # Export dividends separately (as in your example)
    try:
        hist = data.dividends
        if isinstance(hist.index, pd.DatetimeIndex):
            hist.index = hist.index.tz_localize(None)
        hist.to_excel(os.path.join(path, f"{ticker}_dividends.xlsx"))
    except Exception as e:
        print(f"Error exporting dividends: {e}")
# tesqt_yfinance("MSFT")
def test_yfinance(a : str) :
    try:
        data = yf.Ticker(a)
        hist = data.dividends
        info = data.info
        if isinstance(hist.index, pd.DatetimeIndex):
           hist.index = hist.index.tz_localize(None)
        print (hist)
        path = os.path.join(os.path.curdir, 'Exported')
        #bl_sheet = data.balance_sheet
        # bl_sheet.to_excel('MSFT_balance_sheet.xlsx')
        #info = data.analyst_price_targets
        #hist.to_excel(os.path.join(path,'MSFT_dividends.xlsx'))
        #info_df = pd.DataFrame(info.items(),columns=['field','Value'])
       # info_df.to_excel(f"{a}.xlsx")
        #downl=yf.download('MSFT', period='1mo')
        print(info)
       # print(yaml.dump(info, default_flow_style=False))
        # downl.to_excel(os.path.join(path,'MSFT_download.xlsx'))
        # print('Name: '+ data.info['longName'],'\n''city :' + data.info['city'] , '\n' + "website :" + data.info['website'] + '\n' + "sector :" + data.info['sector'])
        # print(hist[['Open', 'High', 'Low', 'Close', 'Volume','Dividends']].round(2))
        # print([info[a] for a in ['longName', 'sector', 'industry', 'country', 'fullTimeEmployees', 'website']])

        # fu_data= data.funds_data
        # print(data.analyst_price_targets)
        spy = yf.Ticker('VOO')
        # print(spy.info)
        # spy.top_holdings
    except Exception as e:
        print(f"Error fetching data: {e}")
        return False
test_yfinance("MSFT")

def test_yfinance_search(company: str):
    a= yf.Search(company,max_results=5)
    b= a.quotes
    pp.pprint(b)
#for i in b:
    #     if i.get('exchDisp') == 'NSE':
    #         print(i.get('symbol'))
#test_yfinance_search('tatamotors')
#pp.pprint( b)# if r["exchDisp"] == 'NSE')
    



#print(n)