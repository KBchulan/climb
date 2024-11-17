import mplfinance as mpf
import matplotlib.pyplot as plt

class ChartDrawer:
    @staticmethod
    def calculate_indicators(df):
        # 确保数据没有无效值
        df = df.fillna(method='ffill').fillna(method='bfill')
        
        # 计算MA
        df['MA5'] = df['Close'].rolling(window=5).mean()
        df['MA10'] = df['Close'].rolling(window=10).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        
        # 计算MACD
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
        
        # 计算RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # 计算KDJ
        low_min = df['Low'].rolling(window=9).min()
        high_max = df['High'].rolling(window=9).max()
        rsv = (df['Close'] - low_min) / (high_max - low_min) * 100
        df['KDJ_K'] = rsv.rolling(window=3).mean()
        df['KDJ_D'] = df['KDJ_K'].rolling(window=3).mean()
        df['KDJ_J'] = 3 * df['KDJ_K'] - 2 * df['KDJ_D']
        
        # 最后处理所有可能的无效值
        df = df.fillna(method='ffill').fillna(method='bfill')
        
        return df

    @staticmethod
    def draw_kline(df):
        """绘制K线图"""
        # 如果数据中没有技术指标，则计算它们
        if 'MA5' not in df.columns:
            df = ChartDrawer.calculate_indicators(df)
        
        # 设置K线图样式
        mc = mpf.make_marketcolors(
            up='red',
            down='green',
            edge='inherit',
            wick='inherit',
            volume='inherit'
        )
        
        # 设置字体大小和样式
        plt.rcParams['font.size'] = 14
        plt.rcParams['axes.titlesize'] = 16
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['legend.fontsize'] = 12
        
        s = mpf.make_mpf_style(
            marketcolors=mc,
            gridstyle='--',
            y_on_right=True,
            rc={
                'font.size': 14,
                'axes.titlesize': 16,
                'axes.labelsize': 14
            }
        )
        
        # 添加技术指标
        add_plots = [
            # 移动平均线
            mpf.make_addplot(df['MA5'], color='blue', width=1),
            mpf.make_addplot(df['MA10'], color='orange', width=1),
            mpf.make_addplot(df['MA20'], color='purple', width=1),
            
            # MACD
            mpf.make_addplot(df['MACD'], color='blue', panel=2),
            mpf.make_addplot(df['MACD_Signal'], color='orange', panel=2),
            mpf.make_addplot(df['MACD_Hist'], type='bar', color='dimgray', panel=2),
            
            # RSI和KDJ
            mpf.make_addplot(df['RSI'], color='red', panel=3),
            mpf.make_addplot(df['KDJ_K'], color='blue', panel=3),
            mpf.make_addplot(df['KDJ_D'], color='orange', panel=3),
            mpf.make_addplot(df['KDJ_J'], color='purple', panel=3)
        ]
        
        # 绘制图表
        fig, axes = mpf.plot(
            df,
            type='candle',
            style=s,
            title='AAPL Stock Analysis',
            ylabel='Price ($)',
            volume=True,
            addplot=add_plots,
            panel_ratios=(6,2,2,2),
            figratio=(16,9),
            figscale=2,
            returnfig=True,
            xrotation=0,
            datetime_format='%Y-%m-%d'
        )
        
        # 调整x轴标签
        for ax in axes:
            if ax is not None:
                ax.tick_params(axis='x', rotation=45)
                ax.grid(True, linestyle='--', alpha=0.5)
        
        # 添加图例
        axes[0].legend(['MA5', 'MA10', 'MA20'], loc='upper left', fontsize=12)
        axes[2].legend(['MACD', 'Signal', 'Histogram'], loc='upper left', fontsize=12)
        axes[3].legend(['RSI', 'K', 'D', 'J'], loc='upper left', fontsize=12)
        
        # 设置标题
        fig.suptitle('AAPL Stock Analysis', fontsize=18, y=0.95)
        
        # 调整子图间距
        fig.tight_layout(rect=[0, 0, 1, 0.95])
        
        # 保存图表
        fig.savefig('stock_chart.png', dpi=200, bbox_inches='tight')
        plt.close(fig)