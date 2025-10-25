import sqlite3

from models.database import DatabaseManager
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QLabel, QDialog
)
from PyQt5.QtCore import Qt
from .order_details_ui import OrderDetailsWindow
from ui.order_form_ui import OrderForm

class OrdersWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Замовлення")
        self.resize(900, 450)


        # Підключення до БД
        db = DatabaseManager()
        self.conn = db.connect()
        self.cursor = self.conn.cursor()



        # --- Основний layout ---
        layout = QVBoxLayout()


        # --- Кнопки ---
        btn_layout = QHBoxLayout()
        self.btn_menu = QPushButton("⬅ Меню")
        self.btn_details = QPushButton("Деталі замовлення")
        self.btn_add = QPushButton("Додати")
        self.btn_edit = QPushButton("Редагувати")
        self.btn_delete = QPushButton("Видалити")


        for btn in [self.btn_menu, self.btn_details, self.btn_add, self.btn_edit, self.btn_delete]:
            btn.setFixedWidth(150)


        btn_layout.addWidget(self.btn_menu)
        btn_layout.addWidget(self.btn_details)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)


        # --- Таблиця ---
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)


        # --- Підключення кнопок ---
        self.btn_menu.clicked.connect(self.go_back)
        self.btn_add.clicked.connect(self.add_order)
        self.btn_edit.clicked.connect(self.edit_order)
        self.btn_delete.clicked.connect(self.delete_order)
        self.btn_details.clicked.connect(self.show_details)


        # --- Завантаження даних ---
        self.load_data()


    def go_back(self):
        """Повернення в головне меню."""
        self.close()
        self.main_window.show()


    def load_data(self):
        """Завантажити дані з таблиці Orders."""
        try:
            self.cursor.execute("""
                SELECT o.id, c.name AS customer_name, o.order_date, o.status, o.total_price
                FROM Orders o
                LEFT JOIN Customers c ON o.customer_id = c.id
            """)
            rows = self.cursor.fetchall()


            headers = ["ID", "Покупець", "Дата замовлення", "Статус", "Сума ($)"]
            self.table.setColumnCount(len(headers))
            self.table.setRowCount(len(rows))
            self.table.setHorizontalHeaderLabels(headers)
            self.table.hideColumn(0)


            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value) if value is not None else "")
                    if col_idx == 4:  # total_price
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.table.setItem(row_idx, col_idx, item)


            self.table.resizeColumnsToContents()


        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зчитати дані:\n{e}")


    def add_order(self):
        self.hide()
        self.form = OrderForm(self)
        self.form.show()


    def edit_order(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Помилка", "Оберіть замовлення для редагування!")
            return
        order_id = int(self.table.item(selected_row, 0).text())
        self.hide()
        self.form = OrderForm(self, order_id)
        self.form.show()



    def delete_order(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Помилка", "Оберіть замовлення для видалення!")
            return
        order_id = int(self.table.item(selected_row, 0).text())
        reply = QMessageBox.question(self, "Підтвердити видалення",
                                     f"Видалити замовлення ID {order_id}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM Orders WHERE id=?", (order_id,))
                self.conn.commit()
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Помилка", f"Не вдалося видалити замовлення:\n{e}")


    def show_details(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Помилка", "Оберіть замовлення для перегляду деталей!")
            return
        order_id = int(self.table.item(selected_row, 0).text())
        self.hide()
        self.details_window = OrderDetailsWindow(order_id, self)
        self.details_window.show()


