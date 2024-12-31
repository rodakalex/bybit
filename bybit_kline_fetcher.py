from datetime import datetime, timedelta
import pandas as pd

class BybitKlineFetcher:
    def __init__(self, session, symbol="BTCUSD"):
        self.session = session
        self.symbol = symbol
        self.end_time = int(datetime.now().timestamp() * 1000)
        self.start_time = int((datetime.now() - timedelta(days=7)).timestamp() * 1000)

    def set_time_period(self, start_days_ago=7):
        self.end_time = int(datetime.now().timestamp() * 1000)
        self.start_time = int((datetime.now() - timedelta(days=start_days_ago)).timestamp() * 1000)

    def get_kline_data(self, interval='D'):
        response = self.session.get_kline(
            category="inverse",
            symbol=self.symbol,
            interval=interval,
            start=self.start_time,
            end=self.end_time
        )
        return response

    def preprocess_kline_data(self, kline_data):
        timestamps = [int(item[0]) for item in kline_data['result']['list']]
        open_prices = [float(item[1]) for item in kline_data['result']['list']]
        high_prices = [float(item[2]) for item in kline_data['result']['list']]
        low_prices = [float(item[3]) for item in kline_data['result']['list']]
        close_prices = [float(item[4]) for item in kline_data['result']['list']]
        volumes = [float(item[5]) for item in kline_data['result']['list']]
        dates = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]

        data = {
            'Date': dates,
            'Open': open_prices,
            'High': high_prices,
            'Low': low_prices,
            'Close': close_prices,
            'Volume': volumes
        }
        df = pd.DataFrame(data)
        df = df.sort_values(by='Date')
        df.set_index('Date', inplace=True)
        return df
