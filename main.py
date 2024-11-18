import sys
from gui import GUI
from database import Database
from chart import ChartDrawer
from config import STOCK_SYMBOL
from stock_crawler import StockCrawler

def initialize_data():
    crawler = StockCrawler(STOCK_SYMBOL)
    
    db = Database()
    
    try:
        stock_data = crawler.fetch_data()
        
        stock_data = ChartDrawer.calculate_indicators(stock_data)
        
        db.save_stock_data(stock_data)
        
        return True
        
    except Exception as e:
        print(f"数据初始化失败: {str(e)}")
        return False    

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--no-fetch':
        print("本次不更新股票数据")
        
    else:
        success = initialize_data()
        if not success:
            print("数据初始化失败")
            sys.exit(1)
                
    app = GUI()
    app.run()