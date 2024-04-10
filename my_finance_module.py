import datetime
import time
import requests

def get_yfinance_data(stock_ticker: str, start_date: str, stop_date: str, listed_in_tw: bool=False) -> dict:
    if listed_in_tw:
        stock_ticker = f"{stock_ticker}.TW"
        start_hour, start_min = 9, 0
        stop_hour, stop_min = 13, 30
    else:
        start_hour, start_min = 9, 30
        stop_hour, stop_min = 16, 0
    start_year, start_month, start_day = [int(e) for e in start_date.split("-")]
    stop_year, stop_month, stop_day = [int(e) for e in stop_date.split("-")]
    start_datetime = datetime.datetime(start_year, start_month, start_day, start_hour, start_min)
    stop_datetime = datetime.datetime(stop_year, stop_month, stop_day, stop_hour, stop_min)
    start_date_unixtime = time.mktime(start_datetime.timetuple())
    stop_date_unixtime = time.mktime(stop_datetime.timetuple())
    period1 = int(start_date_unixtime)
    period2 = int(stop_date_unixtime)
    base_api_url = f"https://query1.finance.yahoo.com/v7/finance/chart/{stock_ticker}"
    request_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    query_str_params = {
        "interval": "1d",
        "period1": period1,
        "period2": period2
    }
    response = requests.get(base_api_url, headers=request_headers, params=query_str_params)
    response_json = response.json()
    print(f"Request status code: {response.status_code}")
    return response_json