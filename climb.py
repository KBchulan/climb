from datetime import datetime
import requests
import json

def climb_data_xinlang(code, timeout, datalen):
    url = f'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={code}&scale={timeout}&ma=5&datalen={datalen}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    
    # 解析 JSON 数据
    result = []
    data = json.loads(response.text)
    
    # 倒叙存入列表
    for match in data[::-1]:
        elem_data = {
            'day': datetime.strptime(match['day'], '%Y-%m-%d %H:%M:%S'),
            'open': float(match['open']),
            'high': float(match['high']),
            'low': float(match['low']),
            'close': float(match['close']),
        }
        result.append(elem_data)
    response.close()
    return result
