import sys
from gui import GUI
from database import Database
from chart import ChartDrawer
from stock_crawler import StockCrawler

def initialize_data():
    crawler = StockCrawler('AAPL')
    
    db = Database()
    
    try:
        stock_data = crawler.fetch_data()
        
        stock_data = ChartDrawer.calculate_indicators(stock_data)
        
        db.save_stock_data(stock_data)
        
        return True
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

def main():
    # 首先初始化数据
    if len(sys.argv) > 1 and sys.argv[1] == '--no-fetch':
        print("跳过数据获取步骤...")
    else:
        success = initialize_data()
        if not success:
            user_input = input("数据初始化失败，是否继续启动GUI？(y/n): ")
            if user_input.lower() != 'y':
                sys.exit(1)
    
    # 启动GUI
    print("启动图形界面...")
    app = GUI()
    app.run()

if __name__ == "__main__":
    main() 