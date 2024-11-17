import time
import requests
import pandas as pd
from datetime import datetime
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

class StockCrawler:
    def __init__(self, symbol):
        self.symbol = symbol
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def fetch_data(self):
        try:
            end_date = int(time.time())
            start_date = end_date - 365 * 24 * 60 * 60
            
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{self.symbol}"
            
            params = {
                'period1': start_date,
                'period2': end_date,
                'interval': '1d',  # 日线数据
                'events': 'history',
                'includeAdjustedClose': 'true'
            }
            
            # 发送请求，添加超时设置
            response = self.session.get(
                url, 
                headers=self.headers, 
                params=params,
                timeout=(5, 15)  # (连接超时, 读取超时)
            )
            
            if response.status_code != 200:
                raise Exception(f"API request failed with status code: {response.status_code}")
            
            # 解析数据
            data = response.json()
            
            if 'chart' not in data or 'result' not in data['chart'] or not data['chart']['result']:
                raise Exception("No data available in response")
            
            result = data['chart']['result'][0]
            timestamps = result['timestamp']
            quote = result['indicators']['quote'][0]
            
            # 创建DataFrame
            df = pd.DataFrame({
                'Date': [datetime.fromtimestamp(ts) for ts in timestamps],
                'Open': quote['open'],
                'High': quote['high'],
                'Low': quote['low'],
                'Close': quote['close'],
                'Volume': quote['volume']
            })
            
            # 设置日期为索引
            df.set_index('Date', inplace=True)
            
            # 处理可能的空值
            df = df.dropna()
            
            if df.empty:
                raise Exception("No valid data available")
            
            return df
            
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to fetch stock data: {str(e)}")
    
    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()
    
    def _format_date(self, date):
        return date.strftime('%Y-%m-%d')