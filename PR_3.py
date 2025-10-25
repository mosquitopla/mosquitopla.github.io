class Phone:
    def __init__(self, model, memory, charge_level):
        self.model = model
        self.memory = memory
        self.__charge_level = charge_level
    
    def to_charge(self, charge):
        if charge <= 0:
            print("Сума заряду має бути додатною.")
        elif self.__charge_level + charge > 100:
            self.__charge_level = 100
            print("Телефон повністю заряджений. Максимальний рівень заряду досягнуто.")
        else:
            self.__charge_level += charge
            print(f"Телефон заряджено на {charge} %. Поточний рівень: {self.__charge_level}%.")

    def _check_charge(self):
        return self.__charge_level
    
    def __phone_info(self):
        return f"Інформація про телефон: {self.model}, Пам'ять: {self.memory}, Рівень заряду: {self.__charge_level}%"

    @property
    def charge_level(self):
        return self.__charge_level

    @charge_level.setter
    def charge_level(self, value):
        if 0 <= value <= 100:
            self.__charge_level = value
        else:
            print("Рівень заряду має бути в межах від 0 до 100")
            
if __name__ == "__main__":
    phone1 = Phone("Samsung S22", "128GB", 40)
    phone2 = Phone("iPhone 14", "256GB", 85)

    print(f"Інформація про {phone1.model}: {phone1.charge_level}% заряду")
    
    phone1.to_charge(30)
    print(f"Новий рівень заряду: {phone1.charge_level}%")
    
    print(f"Інформація про {phone2.model}: {phone2.charge_level}% заряду")
    phone2.to_charge(5)
    print(f"Новий рівень заряду: {phone2.charge_level}%.")
