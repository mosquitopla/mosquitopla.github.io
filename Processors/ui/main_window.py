from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
from .customers_ui import CustomersWindow
from .orders_ui import OrdersWindow
from .products_ui import ProductsWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система замовлень процесорів")
        self.setGeometry(500, 500, 400, 200)


        self.layout = QVBoxLayout()
        self.btn_customers = QPushButton("👤 Клієнти")
        self.btn_orders = QPushButton("📦 Замовлення")
        self.btn_products = QPushButton("💻 Процесори")
        for btn in [self.btn_customers, self.btn_orders, self.btn_products]:
            btn.setFixedSize(250, 50)  # ширина 200px, висота 50px
            btn.setStyleSheet("font-size: 14pt;")  # збільшений шрифт



        self.layout.addWidget(self.btn_customers)
        self.layout.addWidget(self.btn_orders)
        self.layout.addWidget(self.btn_products)


        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)


        # Події
        self.btn_customers.clicked.connect(self.open_customers)
        self.btn_orders.clicked.connect(self.open_orders)
        self.btn_products.clicked.connect(self.open_products)


    def open_customers(self):
        self.win = CustomersWindow(self)
        self.win.show()
        self.hide


    def open_orders(self):
        self.win = OrdersWindow(self)
        self.win.show()


    def open_products(self):
        self.win = ProductsWindow(self)
        self.win.show()
        self.hide()
