import datetime as dt
from typing import Optional

DATE_FORMAT = '%d.%m.%Y'


class Calculator:
    """
    Родительский класс "калькулятор" описывает основные методы:
    добавление записи, подсчёт количества за сегодня и за неделю.
    """
    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record: 'Record') -> None:
        """Метод добавляет запись в список записей."""
        self.records.append(record)

    def get_today_stats(self) -> float:
        """
        Определяет сегодняшнюю дату и считает сумму по записям за сегодня.
        """
        today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == today)

    def get_what_left(self) -> float:
        """Метод считает сколько осталось от лимита."""
        spent_from_limit = self.get_today_stats()
        return self.limit - spent_from_limit

    def get_week_stats(self) -> float:
        today = dt.date.today()
        week_ago = today - dt.timedelta(weeks=1)
        return sum(record.amount for record in self.records
                   if week_ago < record.date <= today)


class CaloriesCalculator(Calculator):
    """наследуем калькулятор каллорий"""
    def get_calories_remained(self) -> str:
        """Определям сколько осталось от лимита."""
        lef_for_today = self.get_what_left()
        if lef_for_today > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но '
                    f'с общей калорийностью не более {lef_for_today} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 74.00
    EURO_RATE = 88.00
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency: str) -> str:
        """
        Вызывает метод get_what_left и выдаёт комментарий
        в зависимости от того, сколько осталось.
        """
        left_for_today = self.get_what_left()
        if left_for_today == 0:
            return 'Денег нет, держись'

        currencies = {
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
            'rub': ('руб', self.RUB_RATE),
        }

        if currency not in currencies:
            raise ValueError('Пожалуйста, выберите одну из нормальных валют.')

        cur_name, cur_rate = currencies[currency]
        left_in_cur = left_for_today / cur_rate
        result = abs(round(left_in_cur, 2))
        if left_in_cur > 0:
            return f'На сегодня осталось {result} {cur_name}'
        return ('Денег нет, держись: '
                f'твой долг - {result} {cur_name}')


class Record:
    """Класс "запись", аккумулирующий данные."""
    def __init__(self, amount: float, comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()
