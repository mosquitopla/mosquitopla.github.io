from .product import Product


class Processor(Product):
    def __init__(self, name, brand, series, cores, threads, socket, price, stock_quantity):
        super().__init__(name, price, stock_quantity)
        self.brand = brand
        self.series = series
        self.cores = cores
        self.threads = threads
        self.socket = socket


    def __str__(self):
        return f"{self.brand} {self.name} ({self.cores}C/{self.threads}T, Socket {self.socket})"
