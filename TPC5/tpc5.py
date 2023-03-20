import re
import sys


class PhoneBooth:
    def __init__(self):
        self.on = False
        self.balance = 0
        self.coin_values = [1, 2, 5, 10, 20, 50, 100, 200]

    def get_balance(self):
        euros = self.balance // 100
        cents = self.balance % 100
        return f"saldo = {euros}e{cents:02d}c"

    def parse_coins(self, coins):
        invalid = []

        for coin in coins:
            match = re.match(r"(\d+)[ce]", coin)
            if match:
                value = int(match.group(1))
                if value in self.coin_values:
                    self.balance += value
                else:
                    invalid.append(coin)
            else:
                invalid.append(coin)

        if invalid:
            msg = f'maq: "{" - moeda inválida; ".join(invalid)}; {self.get_balance()}"'
        else:
            msg = f'maq: "{self.get_balance()}"'
        return msg

    def get_change(self):
        coins = {value: 0 for value in self.coin_values}

        for coin in reversed(self.coin_values):
            while self.balance >= coin:
                self.balance -= coin
                coins[coin] += 1

        msg = f"troco= {coins[200]}x2e, {coins[100]}x1e, {coins[50]}x50c, {coins[20]}x20c, {coins[10]}x10c, {coins[5]}x5c, {coins[2]}x2c, {coins[1]}x1c; Volte sempre!"
        return msg

    def call(self, num):
        if not self.on:
            return 'maq: "O telefone não está em uso!"'

        if not re.match(r"(00)?\d{9}$", num):
            return 'maq: "Número inválido!"'

        if re.match(r"601|641", num):
            return 'maq: "Esse número não é permitido neste telefone. Queira discar novo número!"'

        if num.startswith("00"):
            if self.balance < 150:
                return 'maq: "Saldo insuficiente!"'
            self.balance -= 150
            return f'maq: "{self.get_balance()}"'

        if num.startswith("2"):
            if self.balance < 25:
                return 'maq: "Saldo insuficiente!"'
            self.balance -= 25
            return f'maq: "{self.get_balance()}"'

        if num.startswith("800"):
            return f'maq: "{self.get_balance()}"'

        if num.startswith("808"):
            if self.balance < 10:
                return 'maq: "Saldo insuficiente!"'
            self.balance -= 10
            return f'maq: "{self.get_balance()}"'

    def start(self):
        if self.on:
            return 'maq: "O telefone já está em uso!"'
        self.on = True
        return 'maq: "Introduza moedas."'

    def stop(self):
        if not self.on:
            return 'maq: "O telefone não está em uso!"'
        self.on = False
        msg = f"troco= {self.get_change()}"
        self.balance = 0
        return f'maq: "{msg}"'

    def cancel_call(self):
        if not self.on:
            msg = 'maq: "O telefone não está em uso!"'
        else:
            coins_returned = self.get_change()
            self.balance = 0
            self.on = False
            msg = f'maq: "troco= {coins_returned}; Volte sempre!"'
        return msg


    def handle_input(self, input_str):
        input_str = input_str.strip()
        if not input_str:
            return 'maq: "Introduza moedas."'
        if input_str == "POUSAR":
            return self.stop()
        if input_str == "ABORTAR":
            return self.cancel_call()
        if input_str == "LEVANTAR":
            return self.start()
        if re.match(r"\d{9}", input_str):
            return self.call(input_str)
        if re.match(r"(\d+[ce] )*\d+[ce]$", input_str):
            coins = input_str.split()
            return self.parse_coins(coins)
        return 'maq: "Entrada inválida!"'



def main():
    phone_booth = PhoneBooth()
    print('maq: "Bem-vindo à cabine telefônica!"')
    while True:
        line = input().strip()
        if not line:
            continue
        output = phone_booth.handle_input(line)
        print(output)
        if output == 'maq: "Até a próxima ligação!"':
            break

if __name__ == "__main__":
    main()