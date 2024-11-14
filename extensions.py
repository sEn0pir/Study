import requests
import json

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Некорректное количество: "{amount}". Введите число.')

        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты "{base}".')
        
        url = f'https://api.exchangerate-api.com/v4/latest/{base.upper()}'
        
        try:
            response = requests.get(url)
            data = response.json()
        except requests.exceptions.RequestException:
            raise APIException("Ошибка запроса к API обменного курса.")
        
        if quote.upper() not in data['rates']:
            raise APIException(f'Не удалось обработать валюту "{quote}".')
        
        rate = data['rates'][quote.upper()]
        total = rate * amount
        
        return round(total, 2)
    
    @staticmethod
    def get_available_currencies():
        return "Доступные валюты: евро (EUR), доллар (USD), рубль (RUB)."
