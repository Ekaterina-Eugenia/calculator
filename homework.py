import datetime as dt 
class Calculator:
    def __init__ (self, limit):
        self.limit = limit
        self.records = []
    def add_record(self, record):
        self.records.append(record)
    def get_today_stats(self):  
        return sum(record.amount for record in self.records
                   if record.date == dt.date.today())
    def get_week_stats(self):
        current_date = dt.date.today()
        week_ago = current_date - dt.timedelta(weeks=1)
        return sum(record.amount for record in self.records
                   if week_ago < record.date <= dt.date.today())
class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        eaten_today = self.get_today_stats()
        result = round(self.limit - eaten_today, 2)
        if result > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более ' f'{result} кКал')
        else:
            return ('Хватит есть!')
class CashCalculator(Calculator):
    USD_RATE = 74.00
    EURO_RATE = 88.00
    RUB_RATE = 1.00
    def get_today_cash_remained(self, currancy):
        self.currancy = currancy
        spent_today = self.get_today_stats()
        result = self.limit - spent_today
        currancies = {
            'usd': ['USD', self.USD_RATE],
            'eur': ['Euro', self.EURO_RATE],
            'rub': ['руб', self.RUB_RATE]
        }
        if currancy in currancies:     
            cur_name, cur_rate = currancies[currancy]
            left_in_cur = (result / cur_rate)
            if result == 0:
                return (f'Денег нет, держись')
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
class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        if comment is None:
            self.comment = 'Просто так'
        else:
            self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
