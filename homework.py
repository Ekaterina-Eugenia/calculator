import datetime as dt
from __future__ import annotations


class Calculator:  # создаём родительский класс "калькулятор"
    def __init__(self, limit: union[int, float]) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record) -> list[Record, ...]]:  # добавляем запись
        self.records.append(record)

    def get_today_stats(self) -> float:  # считаем сумму за сегодня
        return sum(record.amount for record in self.records
                   if record.date == dt.date.today())

    def get_week_stats(self) -> union[int, float]:  # считаем сумму за неделю
        current_date = dt.date.today()
        week_ago = current_date - dt.timedelta(weeks=1)
        return sum(record.amount for record in self.records
                   if week_ago < record.date <= dt.date.today())


class CaloriesCalculator(Calculator):  # наследуем калькулятор каллорий
    def get_calories_remained(self) -> str:  # определям сколько осталось
        eaten_today = self.get_today_stats()
        result = round(self.limit - eaten_today, 2)
        if result > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более ' f'{result} кКал')
        else:
            return ('Хватит есть!')


class CashCalculator(Calculator):  # наследуем калькулятор денег
    USD_RATE = 74.00  # определяем валюты
    EURO_RATE = 88.00
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currancy -> str) -> str:  # определяем сколько осталось
        self.currancy = currancy
        spent_today = self.get_today_stats()
        result = self.limit - spent_today  #создаём словарь для пересчёта валют
        currancies = {
            'usd': ['USD', self.USD_RATE],
            'eur': ['Euro', self.EURO_RATE],
            'rub': ['руб', self.RUB_RATE]
        }

        if currancy in currancies:
            cur_name, cur_rate = currancies[currancy]
            left_in_cur = (result / cur_rate)
            if result == 0:
                return ('Денег нет, держись')
            elif result > 0:
                result = (round(left_in_cur, 2))
                return (f'На сегодня осталось {result} {cur_name}')
            else:
                result = abs(round(left_in_cur, 2))
                return ('Денег нет, держись: '
                        'твой долг - '
                        f'{result} {cur_name}')
        else:
            return('Пожалуйста, выберите одну из нормальных валют.')


class Record:  # создаём класс "запись", аккумулирующий данные
    rec_type = tuple[union[int, float], str, datetime]
    def __init__(self, amount: union [int, float], comment: str, date=None) -> rec_type:
        self.amount = amount
        if comment is None:
            self.comment = 'Просто так'
        else:
            self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
