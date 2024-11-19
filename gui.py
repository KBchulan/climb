import os
from database import Database
from chart import ChartDrawer
import dearpygui.dearpygui as dpg
from stock_crawler import StockCrawler

class GUI:
    def __init__(self):
        self.texture_id = 0
        self.db = Database()
        self.chart = ChartDrawer()
        self.crawler = StockCrawler('AAPL')
        
    def fetch_and_save(self):
        try:
            data = self.crawler.fetch_data()
            data = ChartDrawer.calculate_indicators(data)
            self.db.save_stock_data(data)
            dpg.set_value("status", "Data updated successfully!")
            dpg.configure_item("status", color = [0, 255, 0])
            
        except Exception as e:
            dpg.set_value("status", f"Error: {str(e)}")
            dpg.configure_item("status", color = [255, 0, 0])
    
    def show_chart(self):
        try:
            data = self.db.get_all_data()
            if len(data) == 0:
                dpg.set_value("status", "Error: No data available. Please update first!")
                dpg.configure_item("status", color = [255, 0, 0])
                return
            
            self.chart.draw_kline(data)
            
            if os.path.exists("stock_chart.png"):
                if self.texture_id != 0:
                    dpg.delete_item(self.texture_id)
                
                width, height, channels, data = dpg.load_image("stock_chart.png")
                with dpg.texture_registry():
                    self.texture_id = dpg.add_static_texture(width, height, data)
                
                dpg.configure_item("chart_image", texture_tag = self.texture_id)
                dpg.set_value("status", "Chart updated successfully!")
                dpg.configure_item("status", color = [0, 255, 0])
            else:
                dpg.set_value("status", "Error: Chart file not found!")
                dpg.configure_item("status", color = [255, 0, 0])
                print("Chart file not found!")
        except Exception as e:
            print(f"Error in show_chart: {str(e)}")
            dpg.set_value("status", f"Error: {str(e)}")
            dpg.configure_item("status", color = [255, 0, 0])
    
    def run(self):
        dpg.create_context()
        
        dpg.create_viewport(title = "Stock Data Visualization", width = 1200, height = 800)
        dpg.set_viewport_resize_callback(self.resize_callback)
        
        with dpg.texture_registry():
            blank_data = [0] * (100 * 100 * 4)
            self.texture_id = dpg.add_static_texture(100, 100, blank_data)
        
        with dpg.window(label = "Stock Analysis Panel", width = 1180, height = 780):
            with dpg.group(horizontal = True):
                dpg.add_button(label = "Update Data", callback = self.fetch_and_save, width = 150, height = 40)
                dpg.add_spacer(height = 5)
                dpg.add_button(label = "Show Chart", callback = self.show_chart, width = 150, height = 40)
            
            dpg.add_spacer(height = 10)
            dpg.add_separator()
            dpg.add_spacer(height = 10)
            
            with dpg.group(horizontal = True):
                dpg.add_text("Status: ", color = [255, 255, 255])
                dpg.add_text("System Ready", tag = "status", color = [0, 255, 0])
            
            dpg.add_spacer(height = 10)
            
            with dpg.group():
                dpg.add_text("K-Line Chart:")
                dpg.add_image(self.texture_id, tag = "chart_image", width = 1100, height = 600)
        
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
    
    def resize_callback(self, sender, app_data):
        new_width = app_data[0]
        new_height = app_data[1]
        dpg.configure_item("chart_image", width = new_width-100, height = new_height - 200)
        