import pandas as pd

class Indicators:
    @staticmethod
    def adx_recommendation(adx, plus_di, minus_di):
        """Provide recommendation based on ADX, +DI, and -DI values."""
        if adx < 20:
            return "Neutral"
        elif adx >= 20 and plus_di > minus_di:
            if adx < 40:
                return "Buy"
            else:  # adx >= 40
                return "Strong Buy"
        elif adx >= 20 and minus_di > plus_di:
            if adx < 40:
                return "Sell"
            else:  # adx >= 40
                return "Strong Sell"
        return "Neutral"

    @staticmethod
    def calculate_adx(high_prices, low_prices, close_prices, di_len=14, adx_len=14):
        """Calculate Average Directional Index (ADX)."""
        # Calculate directional movements
        up = high_prices.diff()
        down = -low_prices.diff()

        plus_dm = up.where((up > down) & (up > 0), 0)
        minus_dm = down.where((down > up) & (down > 0), 0)

        # Calculate True Range (TR)
        tr1 = high_prices - low_prices
        tr2 = (high_prices - close_prices.shift(1)).abs()
        tr3 = (low_prices - close_prices.shift(1)).abs()
        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        # Smooth True Range, +DM, -DM using RMA
        smoothed_tr = Indicators.calculate_rma(true_range, di_len)
        smoothed_plus_dm = Indicators.calculate_rma(plus_dm, di_len)
        smoothed_minus_dm = Indicators.calculate_rma(minus_dm, di_len)

        # Calculate +DI and -DI
        plus_di = 100 * smoothed_plus_dm / smoothed_tr
        minus_di = 100 * smoothed_minus_dm / smoothed_tr

        # Handle potential NaN values from division
        plus_di = plus_di.fillna(0)
        minus_di = minus_di.fillna(0)

        # Calculate DX
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di).replace(0, 1)

        # Smooth DX to get ADX
        adx = Indicators.calculate_rma(dx, adx_len)

        return adx, plus_di, minus_di

    @staticmethod
    def calculate_rma(series, period):
        """Calculate Rolling Moving Average (RMA), equivalent to ta.rma in Pine Script."""
        return series.ewm(alpha=1 / period, adjust=False).mean()

    @staticmethod
    def stochastic_recommendation(k, d):
        """Provide recommendation based on Stochastic Oscillator (%K and %D)."""
        if k < 20 and d < 20:
            return "Strong Buy"
        elif 20 <= k < 40 and 20 <= d < 40:
            return "Buy"
        elif 40 <= k <= 60 and 40 <= d <= 60:
            return "Neutral"
        elif 60 < k <= 80 and 60 < d <= 80:
            return "Sell"
        else:  # k > 80 and d > 80
            return "Strong Sell"

    @staticmethod
    def cci_recommendation(cci):
        """Provide recommendation based on CCI value."""
        if cci < -150:
            return "Strong Buy"
        elif -150 <= cci < -100:
            return "Buy"
        elif -100 <= cci <= 100:
            return "Neutral"
        elif 100 < cci <= 150:
            return "Sell"
        else:  # cci > 150
            return "Strong Sell"


    @staticmethod
    def adx_recommendation(adx, plus_di, minus_di):
        """Provide recommendation based on ADX, +DI, and -DI values."""
        if adx < 20:
            return "Neutral"
        elif adx >= 20:
            if plus_di > minus_di:
                return "Buy"
            elif minus_di > plus_di:
                return "Sell (Strong Trend)"
        return "Neutral"

    @staticmethod
    def rsi_recommendation(rsi):
        if rsi < 30:
            return "Активно покупать"
        elif 30 <= rsi < 40:
            return "Покупать"
        elif 40 <= rsi <= 60:
            return "Нейтрально"
        elif 60 < rsi <= 70:
            return "Продавать"
        else:  # rsi > 70
            return "Активно продавать"

    @staticmethod
    def calculate_rsi(close_prices, period=14):
        delta = close_prices.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi = rsi.where(avg_loss != 0, 100)
        rsi = rsi.where(avg_gain != 0, 0)

        return rsi


    @staticmethod
    def calculate_stochastic(close_prices, high_prices, low_prices, period_k=14, smooth_k=1, period_d=3):
        lowest_low = low_prices.rolling(window=period_k).min()
        highest_high = high_prices.rolling(window=period_k).max()

        k = 100 * ((close_prices - lowest_low) / (highest_high - lowest_low))
        k_smoothed = k.rolling(window=smooth_k).mean()
        d = k_smoothed.rolling(window=period_d).mean()

        return k_smoothed, d

    @staticmethod
    def calculate_cci(close_prices, high_prices, low_prices, period=20):
        typical_price = (close_prices + high_prices + low_prices) / 3
        sma = typical_price.rolling(window=period).mean()
        mean_deviation = typical_price.rolling(window=period).apply(
            lambda x: (abs(x - x.mean())).mean(), raw=False)
        cci = (typical_price - sma) / (0.015 * mean_deviation)
        return cci

    @staticmethod
    def calculate_ao(high_prices, low_prices):
        """Calculate Awesome Oscillator (AO)."""
        # Расчёт hl2, среднее между High и Low
        hl2 = (high_prices + low_prices) / 2
        
        # Простое скользящее среднее (SMA) для 5 и 34 периодов
        sma_5 = hl2.rolling(window=5).mean()
        sma_34 = hl2.rolling(window=34).mean()
        
        # Разница между SMA
        ao = sma_5 - sma_34
        
        # Округление результата до 5 знаков для точности
        return ao.round(5)


    @staticmethod
    def ao_recommendation(current_ao, ao_diff, timeframe="yearly"): # TODO: указать таймфрейм в аргументах
        """
        Рекомендации на основе AO с учётом таймфрейма.
        - timeframe: 'daily', 'weekly', 'monthly', 'yearly'
        """
        # Установим пороги для нейтрального сигнала в зависимости от таймфрейма
        if timeframe == "yearly":
            ao_threshold = 5000  # Годовой график
            diff_threshold = 1000
        elif timeframe == "monthly":
            ao_threshold = 1000  # Месячный график
            diff_threshold = 500
        else:
            ao_threshold = 100  # Ежедневный/недельный график
            diff_threshold = 50

        # Нейтральный сигнал
        if abs(current_ao) < ao_threshold and abs(ao_diff) < diff_threshold:
            return "Neutral"

        # Сигнал покупки
        if ao_diff > 0:
            return "Buy"

        # Сигнал продажи
        if ao_diff < 0:
            return "Sell"

        return "Neutral"
