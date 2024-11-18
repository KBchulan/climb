import pandas as pd
import mysql.connector
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute('DROP TABLE IF EXISTS apple')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS apple (
                date DATE PRIMARY KEY,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume BIGINT,
                ma5 FLOAT,
                ma10 FLOAT,
                ma20 FLOAT,
                macd FLOAT,
                macd_signal FLOAT,
                macd_hist FLOAT,
                rsi FLOAT,
                kdj_k FLOAT,
                kdj_d FLOAT,
                kdj_j FLOAT
            )
        ''')
        self.conn.commit()
    
    def save_stock_data(self, df):
        df = df.where(pd.notnull(df), None)
        
        for index, row in df.iterrows():
            sql = '''INSERT INTO apple (
                    date, open, high, low, close, volume,
                    ma5, ma10, ma20, macd, macd_signal, macd_hist,
                    rsi, kdj_k, kdj_d, kdj_j
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            values = (
                index.date(), 
                float(row['Open']) if row['Open'] is not None else None,
                float(row['High']) if row['High'] is not None else None,
                float(row['Low']) if row['Low'] is not None else None,
                float(row['Close']) if row['Close'] is not None else None,
                int(row['Volume']) if row['Volume'] is not None else None,
                float(row['MA5']) if row['MA5'] is not None else None,
                float(row['MA10']) if row['MA10'] is not None else None,
                float(row['MA20']) if row['MA20'] is not None else None,
                float(row['MACD']) if row['MACD'] is not None else None,
                float(row['MACD_Signal']) if row['MACD_Signal'] is not None else None,
                float(row['MACD_Hist']) if row['MACD_Hist'] is not None else None,
                float(row['RSI']) if row['RSI'] is not None else None,
                float(row['KDJ_K']) if row['KDJ_K'] is not None else None,
                float(row['KDJ_D']) if row['KDJ_D'] is not None else None,
                float(row['KDJ_J']) if row['KDJ_J'] is not None else None
            )
            try:
                self.cursor.execute(sql, values)
            except Exception as e:
                print(f"Error inserting row for date {index.date()}: {str(e)}")
                continue
        
        self.conn.commit()
    
    def get_all_data(self):
        self.cursor.execute('''
            SELECT date, open, high, low, close, volume,
                   ma5, ma10, ma20, macd, macd_signal, macd_hist,
                   rsi, kdj_k, kdj_d, kdj_j
            FROM apple 
            ORDER BY date
        ''')
        rows = self.cursor.fetchall()
        
        df = pd.DataFrame(rows, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume',
                                       'MA5', 'MA10', 'MA20', 'MACD', 'MACD_Signal', 'MACD_Hist',
                                       'RSI', 'KDJ_K', 'KDJ_D', 'KDJ_J'])
        
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        
        float_columns = ['Open', 'High', 'Low', 'Close', 'MA5', 'MA10', 'MA20',
                        'MACD', 'MACD_Signal', 'MACD_Hist', 'RSI', 'KDJ_K', 'KDJ_D', 'KDJ_J']
        for col in float_columns:
            df[col] = df[col].astype(float)
        df['Volume'] = df['Volume'].astype(int)
        
        return df
    
    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()