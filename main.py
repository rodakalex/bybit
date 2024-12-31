import argparse
from pybit.unified_trading import HTTP
from bybit_kline_fetcher import BybitKlineFetcher
from plotting import Plotter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot specific indicator chart.")
    parser.add_argument("indicator", choices=["rsi", "stochastic", "cci", "adx"], help="The type of indicator to plot.")
    args = parser.parse_args()

    session = HTTP(testnet=False)
    kline_fetcher = BybitKlineFetcher(session)
    kline_fetcher.set_time_period(start_days_ago=365)

    kline_data = kline_fetcher.get_kline_data(interval='D')
    df = kline_fetcher.preprocess_kline_data(kline_data)

    plotter = Plotter(kline_fetcher.symbol)
    plotter.plot_indicator(df, args.indicator)
