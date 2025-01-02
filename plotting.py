import mplfinance as mpf

from indicators import Indicators

class Plotter:
    def __init__(self, symbol):
        self.symbol = symbol

    def plot_indicator(self, df, indicator_type):
        add_plot = []
        recommendation = "Нет данных"

        if indicator_type == "rsi":
            df['RSI'] = Indicators.calculate_rsi(df['Close'])
            recommendation = Indicators.rsi_recommendation(df['RSI'].iloc[-1])
            print(f"RSI values:\n{df[['Close', 'RSI']].tail(10)}")
            print(f"Recommendation: {recommendation}")
            add_plot.append(mpf.make_addplot(df['RSI'], panel=1, color='blue', ylabel='RSI'))

        elif indicator_type == "stochastic":
            df['%K'], df['%D'] = Indicators.calculate_stochastic(df['Close'], df['High'], df['Low'])
            recommendation = Indicators.stochastic_recommendation(df['%K'].iloc[-1], df['%D'].iloc[-1])
            print(f"Stochastic values (%K and %D):\n{df[['Close', '%K', '%D']].tail(10)}")
            print(f"Recommendation: {recommendation}")
            add_plot.append(mpf.make_addplot(df['%K'], panel=1, color='green', ylabel='Stochastic'))
            add_plot.append(mpf.make_addplot(df['%D'], panel=1, color='orange'))

        elif indicator_type == "cci":
            df['CCI'] = Indicators.calculate_cci(df['Close'], df['High'], df['Low'])
            recommendation = Indicators.cci_recommendation(df['CCI'].iloc[-1])
            print(f"CCI values:\n{df[['Close', 'CCI']].tail(10)}")
            print(f"Recommendation: {recommendation}")
            add_plot.append(mpf.make_addplot(df['CCI'], panel=1, color='blue', ylabel='CCI'))

        elif indicator_type == "adx":
            df['ADX'], df['+DI'], df['-DI'] = Indicators.calculate_adx(df['High'], df['Low'], df['Close'])
            recommendation = Indicators.adx_recommendation(df['ADX'].iloc[-1], df['+DI'].iloc[-1], df['-DI'].iloc[-1])
            print(f"ADX values:\n{df[['Close', 'ADX', '+DI', '-DI']].tail(10)}")
            print(f"Recommendation: {recommendation}")
            add_plot.append(mpf.make_addplot(df['ADX'], panel=1, color='red', ylabel='ADX'))
            add_plot.append(mpf.make_addplot(df['+DI'], panel=1, color='green', ylabel='+DI'))
            add_plot.append(mpf.make_addplot(df['-DI'], panel=1, color='orange', ylabel='-DI'))

        elif indicator_type == "ao":
            df['AO'] = Indicators.calculate_ao(df['High'], df['Low'])
            recommendation = Indicators.ao_recommendation(df['AO'].iloc[-1], df['AO'].diff().iloc[-1])
            print(f"AO values:\n{df[['Close', 'AO']].tail(10)}")
            print(f"Recommendation: {recommendation}")
            
            # Генерация цветов для гистограммы AO
            colors = ['green' if val > 0 else 'red' for val in df['AO']]
            
            # Добавление AO с цветами
            add_plot.append(
                mpf.make_addplot(df['AO'], panel=1, type='bar', color=colors, ylabel='AO')
            )

        mpf.plot(df,
                type='candle',
                volume=False,
                style='charles',
                title=f"{self.symbol} Candlestick Chart with {indicator_type.upper()}",
                ylabel='Price (USD)',
                addplot=add_plot,
                savefig=dict(fname=f'candlestick_with_{indicator_type}_chart.png', dpi=300),
                figscale=1.5,
                figratio=(16, 9))

        return recommendation
