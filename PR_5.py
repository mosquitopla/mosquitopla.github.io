from abc import ABC, abstractmethod

class Payment(ABC):
    def __init__(self, amount, balance = 0):
        self.amount = amount
        self.balance = balance
        
    @abstractmethod
    def pay(self):
        pass
    
    @abstractmethod
    def deposit(self, amount):
        pass
    
class CashPayment(Payment):
    def pay(self):
        if self.amount <= self.balance:
            self.balance -= self.amount
            return f"Олата готівкою {self.amount} грн. прийнято. Баланс: {self.balance} грн."
        else:
            return f"Олата готівкою відхилена. Недостатньо грошів(потрібно{self.amount}, на балансі {self.balance} грн.)"

    def deposit(self, amount):
        self.balance += amount
        return f"Гаманець поповнено готівкою на {amount} грн. Баланс: {self.balance}"

class CardPayment(Payment):
    def __init__(self, owner, number, amount, balance):
        super().__init__(amount, balance)
        self.owner = owner
        self.number = number
        
    def pay(self):
        last_four = self.number[-4:]
        if self.amount <= self.balance:
            self.balance -= self.amount 
            last_four = self.number[-4:]
            return f"Оплата карткою: {self.amount} грн прийнята.  Гроші на Картці **** {last_four} списані. Баланс: {self.balance} грн."
        else:
            return f"На картці **** {last_four} недостатньо коштів. Потрібна сума: {self.amount} грн. Баланс: {self.balance} грн"
    
    def deposit(self, amount):
        self.balance += amount
        return f"{self.owner} поповнив рахунок на {amount}. Баланс: {self.balance}"
    
    
if __name__ == "__main__":
    try:
        transaction = Payment(300)
    except TypeError as e:
        print("Помилка:", e)
        
    transaction1 = CashPayment(amount = 150, balance = 200)
    transaction2 = CashPayment(amount = 1000, balance = 50)
    transaction3 = CardPayment(amount = 500, owner="Олена Петрівна", number = "5555444433332222", balance = 800)
    
    print(transaction1.pay())
    print(transaction2.pay())
    print(transaction2.deposit(1200))
    print(transaction2.pay())
    
    print(transaction3.pay())
    transaction3.amount = 400
    print(transaction3.pay())