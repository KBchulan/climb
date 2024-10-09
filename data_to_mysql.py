from datetime import datetime
import mysql.connector

def save_to_mysql(data, database):
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "whx051021",
        database = database
    )
    
    cursor = connection.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS img_gl (
        id INT AUTO_INCREMENT PRIMARY KEY,
        day DATETIME,
        open FLOAT,
        close FLOAT,
        high FLOAT,
        low FLOAT
    )
    """)
    
    cursor.execute("TRUNCATE TABLE img_gl")

    for entry in data:
        formatted_day = entry['day'].strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute("""
        INSERT INTO img_gl (day, open, close, high, low) 
        VALUES(%s, %s, %s, %s, %s)
        """, 
        (formatted_day, entry['open'], entry['close'], entry['high'], entry['low'])
    )

    connection.commit()
    cursor.close()
    connection.close()