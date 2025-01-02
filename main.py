import argparse
from pybit.unified_trading import HTTP
from bybit_kline_fetcher import BybitKlineFetcher
from plotting import Plotter


# Таблица соответствия времени и интервалов
INTERVAL_MAPPING = {
    "1m": {"interval": "1", "days": 1},
    "5m": {"interval": "5", "days": 5},
    "15m": {"interval": "15", "days": 15},
    "30m": {"interval": "30", "days": 30},
    "1h": {"interval": "60", "days": 90},
    "2h": {"interval": "120", "days": 180},
    "4h": {"interval": "240", "days": 180},
    "1d": {"interval": "D", "days": 365},
    "1w": {"interval": "W", "days": 730},
    "1mo": {"interval": "M", "days": 1825},
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot specific indicator chart.")
    parser.add_argument("indicator", choices=["rsi", "stochastic", "cci", "adx", "ao"], help="The type of indicator to plot.")
    parser.add_argument("--symbol", default="BTCUSD", help="The trading pair symbol (default: BTCUSD).")
    parser.add_argument("--timeframe", choices=INTERVAL_MAPPING.keys(), default="1m", help="Choose timeframe (default: 1m).")
    args = parser.parse_args()

    # Выбор временного интервала и диапазона
    timeframe = INTERVAL_MAPPING[args.timeframe]
    interval = timeframe["interval"]
    days = timeframe["days"]

    # Инициализация Bybit Kline Fetcher
    session = HTTP(testnet=False)
    kline_fetcher = BybitKlineFetcher(session, symbol=args.symbol)
    kline_fetcher.set_time_period(start_days_ago=days)

    # Получение данных и построение графика
    kline_data = kline_fetcher.get_kline_data(interval=interval)
    df = kline_fetcher.preprocess_kline_data(kline_data)

    plotter = Plotter(kline_fetcher.symbol)
    plotter.plot_indicator(df, args.indicator)
