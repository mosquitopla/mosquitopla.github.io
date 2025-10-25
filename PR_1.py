class Phone:
    cpu_type = "Dimensity"
    def __init__(self, model, memory, battery):
        self.model = model
        self.memory = memory
        self.battery = battery
        
    def make_a_call(self):
        print(f"{self.model} робить дзвінок!")
        
    def open_an_app(self):
        print(f"{self.model} відкриває додаток!")
        
    def calculate_calls(self, duration):
        number_of_calls = self.battery // duration
        print(f"{number_of_calls} дзвінків вистачить на {duration} хв.")
        
        
    @classmethod
    def show_cpu_type(cls):
        print(f"Тип процесора: {cls.cpu_type}")
        
    @staticmethod
    def Call():
        print("Музика")
        
phone1 = Phone("Apple", "4 Гб", 70)
phone2 = Phone("Samsung", "5 Гб", 100)
phone3 = Phone("Xiaomi", "6 Гб", 50)

phone1.make_a_call()
phone1.open_an_app()
phone1.calculate_calls(5)

Phone.show_cpu_type()
Phone.Call()

phone2.make_a_call()
phone2.open_an_app()
phone2.calculate_calls(3)

phone3.make_a_call()
phone3.open_an_app()
phone3.calculate_calls(6)