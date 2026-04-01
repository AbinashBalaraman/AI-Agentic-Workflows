import yfinance as yf
import pprint as pp

def get_stock_news(a:str) -> dict:
    """Get full news about given company"""
    ticker = yf.Ticker(a)
    info = ticker.news
    # pp.pprint(str(info))
    print(type(info))
    # print (a)
    news=()
    aa={}
    for l in range(len(info)):
        try:
            aa[f"News no {l+1}"] =info[l]["content"]["summary"]
        except Exception as e :
            pass
    return aa
print(get_stock_news("MSFT"))
