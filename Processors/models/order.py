class Order:
    order_counter = 0


    def __init__(self, customer):
        Order.order_counter += 1
        self.id = Order.order_counter
        self.customer = customer
        self.items = []


    def add_item(self, product, quantity):
        if product.reduce_stock(quantity):
            self.items.append((product, quantity))
        else:
            print("Недостатньо на складі!")


    def calculate_total(self):
        return sum(product.get_price() * qty for product, qty in self.items)


    def __str__(self):
        return f"Order #{self.id} for {self.customer.name}, Total: {self.calculate_total()} USD"
