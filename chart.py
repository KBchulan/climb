import mplfinance as mpf
import matplotlib.pyplot as plt

class ChartDrawer:
    @staticmethod
    def calculate_indicators(df):
        df = df.ffill().bfill()
        
        df['MA5'] = df['Close'].rolling(window = 5).mean()
        df['MA10'] = df['Close'].rolling(window = 10).mean()
        df['MA20'] = df['Close'].rolling(window = 20).mean()
        
        exp1 = df['Close'].ewm(span = 12, adjust = False).mean()
        exp2 = df['Close'].ewm(span = 26, adjust = False).mean()
        df['MACD'] = exp1 - exp2
        df['MACD_Signal'] = df['MACD'].ewm(span = 9, adjust = False).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
        
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window = 14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window = 14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        low_min = df['Low'].rolling(window = 9).min()
        high_max = df['High'].rolling(window = 9).max()
        rsv = (df['Close'] - low_min) / (high_max - low_min) * 100
        df['KDJ_K'] = rsv.rolling(window = 3).mean()
        df['KDJ_D'] = df['KDJ_K'].rolling(window = 3).mean()
        df['KDJ_J'] = 3 * df['KDJ_K'] - 2 * df['KDJ_D']
        
        df = df.ffill().bfill()
        
        return df

    @staticmethod
    def draw_kline(df):
        mc = mpf.make_marketcolors(
            up = 'red',
            down = 'green',
            edge = 'inherit',
            wick = 'inherit',
            volume = 'inherit'
        )
        
        plt.rcParams['font.size'] = 14
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['legend.fontsize'] = 12
        
        s = mpf.make_mpf_style(
            marketcolors = mc,
            gridstyle = '--',
            y_on_right = True,
            rc = {
                'font.size': 14,
                'axes.titlesize': 16,
                'axes.labelsize': 14
            }
        )
        
        add_plots = [
            mpf.make_addplot(df['MA5'], color = 'blue', width = 1, panel = 0, secondary_y = False),
            mpf.make_addplot(df['MA10'], color = 'orange', width = 1, panel = 0, secondary_y = False),
            mpf.make_addplot(df['MA20'], color = 'purple', width = 1, panel = 0, secondary_y = False),
            
            mpf.make_addplot(df['MACD'], color = 'blue', panel = 1, secondary_y = False, ylabel = 'MACD'),
            mpf.make_addplot(df['MACD_Signal'], color = 'orange', panel = 1, secondary_y = False),
            mpf.make_addplot(df['MACD_Hist'], type = 'bar', color = 'dimgray', panel = 1, secondary_y = False),
            
            mpf.make_addplot(df['RSI'], color = 'red', panel = 3, secondary_y = False),
            mpf.make_addplot(df['KDJ_K'], color = 'blue', panel = 3, secondary_y = False),
            mpf.make_addplot(df['KDJ_D'], color = 'orange', panel = 3, secondary_y = False),
            mpf.make_addplot(df['KDJ_J'], color = 'purple', panel = 3, secondary_y = False)
        ]
        
        fig, axes = mpf.plot(
            df,
            type = 'candle',
            style = s,
            title = 'AAPL Stock Analysis',
            ylabel = 'Price ($)',
            volume = True,
            addplot = add_plots,
            panel_ratios = (6,2,2,2),
            figratio = (16,9),
            figscale = 2,
            returnfig = True,
            xrotation = 0,
            datetime_format = '%Y-%m-%d',
            volume_panel = 2
        )
        
        for ax in axes:
            if ax is not None:
                ax.tick_params(axis = 'x', rotation = 45)
                ax.grid(True, linestyle = '--', alpha = 0.5)
                if hasattr(ax, 'legend_') and ax.legend_:
                    ax.legend_.remove()
        
        axes[0].legend(['MA5', 'MA10', 'MA20'], 
                      loc = 'upper left', fontsize = 12)
        
        if len(axes) > 2:
            axes[1].legend(['MACD', 'Signal', 'Histogram'], 
                          loc = 'upper left', fontsize = 8)
        
        if len(axes) > 3:
            axes[3].legend(['RSI', 'K', 'D', 'J'], 
                          loc = 'upper left', fontsize = 12)
        
        axes[0].set_title('Price & MA', fontsize = 8, pad = 10)
        axes[1].set_title('MACD', fontsize = 8, pad = 10)
        axes[2].set_title('Volume', fontsize = 8, pad = 10)
        axes[3].set_title('RSI & KDJ', fontsize = 8, pad = 10)
        
        fig.suptitle('AAPL K Line', fontsize = 18, y = 0.95)
        
        fig.tight_layout(rect = [0, 0, 1, 0.95])
        
        fig.savefig('stock_chart.png', dpi = 200, bbox_inches = 'tight')
        plt.close(fig)