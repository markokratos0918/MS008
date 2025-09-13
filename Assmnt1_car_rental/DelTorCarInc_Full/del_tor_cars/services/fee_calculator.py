class FeeCalculator:
    @staticmethod
    def calc(days: int, daily_rate: float, extras: float = 0.0):
        base = round(days * daily_rate, 2)
        extras_total = round(extras, 2)
        total = round(base + extras_total, 2)
        return base, extras_total, total