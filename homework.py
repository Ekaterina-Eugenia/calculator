import datetime as dt
from typing import Optional


class Calculator:
    """создаём родительский класс калькулятор"""
    today = dt.date.today()

    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record: 'Record') -> None:
        """добавляем запись"""
        self.records.append(record)

    def get_today_stats(self) -> float:
        """считаем сумму за сегодня"""
        return sum(record.amount for record in self.records
                   if record.date == self.today)

    def get_what_left(self) -> float:
        spent_from_limit = self.get_today_stats()
        return self.limit - spent_from_limit

    def get_week_stats(self) -> float:
        """считаем сумму за неделю"""
        week_ago = self.today - dt.timedelta(weeks=1)
        return sum(record.amount for record in self.records
                   if week_ago < record.date <= self.today)


class CaloriesCalculator(Calculator):
    """наследуем калькулятор каллорий"""
    def get_calories_remained(self) -> str:
        """определям сколько осталось от лимита"""
        lef_for_today = self.get_what_left()
        if lef_for_today > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{lef_for_today} кКал')
        else:
            return ('Хватит есть!')


class CashCalculator(Calculator):
    """наследуем калькулятор денег"""
    USD_RATE = 74.00  # определяем валюты
    EURO_RATE = 88.00
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currancy: str) -> str:
        """определяем сколько осталось"""
        left_for_today = self.get_what_left()
        if left_for_today == 0:
            return 'Денег нет, держись'

        currancies = {
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
            'rub': ('руб', self.RUB_RATE),
        }

        if currancy in currancies:
            cur_name, cur_rate = currancies[currancy]
            left_in_cur = left_for_today / cur_rate
            if left_in_cur > 0:
                result = (round(left_in_cur, 2))
                return (f'На сегодня осталось {result} {cur_name}')
            else:
                result = abs(round(left_in_cur, 2))
                return ('Денег нет, держись: '
                        'твой долг - '
                        f'{result} {cur_name}')
        else:
            return('Пожалуйста, выберите одну из нормальных валют.')


class Record:
    """создаём класс "запись", аккумулирующий данные"""
    def __init__(self, amount: float, comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        DATE_FORMAT = '%d.%m.%Y'
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()
