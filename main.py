import pprint
from pybit.unified_trading import HTTP
from datetime import datetime, timedelta
import pandas as pd
import mplfinance as mpf

class BybitKlineFetcher:
    def __init__(self, testnet=False, symbol="BTCUSD"):
        self.session = HTTP(testnet=testnet)
        self.symbol = symbol
        self.end_time = int(datetime.now().timestamp() * 1000)
        self.start_time = int((datetime.now() - timedelta(days=7)).timestamp() * 1000)

    def set_time_period(self, start_days_ago=7, end_days_ago=0):
        """Устанавливает период времени для запроса данных Kline."""
        self.end_time = int(datetime.now().timestamp() * 1000)
        self.start_time = int((datetime.now() - timedelta(days=start_days_ago)).timestamp() * 1000)

    def get_kline_data(self, interval='D'):
        """Получает данные Kline для заданного интервала времени."""
        response = self.session.get_kline(
            category="inverse",
            symbol=self.symbol,
            interval=interval,
            start=self.start_time,
            end=self.end_time
        )
        return response

    def plot_candlestick(self, kline_data):
        """Строит график японских свечей на основе данных Kline."""
        # Преобразование данных в формат DataFrame
        timestamps = [int(item[0]) for item in kline_data['result']['list']]
        open_prices = [float(item[1]) for item in kline_data['result']['list']]
        high_prices = [float(item[2]) for item in kline_data['result']['list']]
        low_prices = [float(item[3]) for item in kline_data['result']['list']]
        close_prices = [float(item[4]) for item in kline_data['result']['list']]
        volumes = [float(item[5]) for item in kline_data['result']['list']]

        # Преобразование времени из таймстемпов в читаемый формат
        dates = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]

        # Создание DataFrame для свечного графика
        data = {
            'Date': dates,
            'Open': open_prices,
            'High': high_prices,
            'Low': low_prices,
            'Close': close_prices,
            'Volume': volumes
        }
        df = pd.DataFrame(data)
        
        # Сортировка по дате
        df = df.sort_values(by='Date')
        df.set_index('Date', inplace=True)

        # Построение свечного графика
        mpf.plot(df, type='candle', volume=True, style='charles', title=f"{self.symbol} Candlestick Chart", ylabel='Price (USD)', ylabel_lower='Volume')


if __name__ == "__main__":
    kline_fetcher = BybitKlineFetcher()
    kline_fetcher.set_time_period(start_days_ago=30)
    kline_data = kline_fetcher.get_kline_data(interval='D')
    pprint.pprint(kline_data)
    kline_fetcher.plot_candlestick(kline_data)
