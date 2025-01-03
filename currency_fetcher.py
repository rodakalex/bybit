import argparse
from pybit.unified_trading import HTTP


class CurrencyFetcher:
    def __init__(self, testnet=True):
        """
        Инициализация сессии для работы с API Bybit.
        """
        self.session = HTTP(testnet=testnet)

    def get_available_symbols(self, category="spot"):
        """
        Получение списка доступных торговых пар.

        :param category: Категория рынка (linear, inverse, spot, option)
        :return: Список словарей с информацией о символах
        :raises Exception: В случае ошибки API
        """
        response = self.session.get_tickers(category=category)
        
        # Проверяем успешность запроса
        if response.get("retCode") != 0:
            raise Exception(f"Ошибка API: {response.get('retMsg', 'Неизвестная ошибка')}")

        return response['result']['list']


if __name__ == '__main__':
    # Парсер аргументов
    parser = argparse.ArgumentParser(
        description="Получение списка валют с Bybit API.",
        epilog="Пример использования:\n"
               "  python currency_fetcher.py\n"
               "  python currency_fetcher.py --category linear --limit all\n"
               "  python currency_fetcher.py --limit 5",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--category",
        default="spot",
        choices=["linear", "inverse", "spot", "option"],
        help="Категория рынка (по умолчанию: spot)."
    )
    parser.add_argument(
        "--limit",
        default=10,
        help="Количество символов для отображения (по умолчанию: 10). Укажите 'all' для вывода всех.",
    )
    args = parser.parse_args()

    # Инициализация объекта для работы с API
    fetcher = CurrencyFetcher(testnet=True)

    try:
        # Получаем список доступных валют
        symbols = fetcher.get_available_symbols(category=args.category)

        # Обработка аргумента limit
        if args.limit == "all":
            limit = len(symbols)
        else:
            try:
                limit = int(args.limit)
                if limit <= 0 or limit > len(symbols):
                    raise ValueError("Число должно быть положительным и не превышать количество символов.")
            except ValueError as e:
                print(f"Ошибка параметра --limit: {e}. Используется значение по умолчанию: 10.")
                limit = 10

        # Вывод информации о символах
        print(f"Найдено {len(symbols)} символов. Отображается {limit} из них:\n")
        for symbol in symbols[:limit]:
            print(f"Символ: {symbol['symbol']}, Последняя цена: {symbol['lastPrice']}, Объем за 24ч: {symbol['volume24h']}")

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
