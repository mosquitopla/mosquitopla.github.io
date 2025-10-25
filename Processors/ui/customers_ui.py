import sqlite3
from models.database import DatabaseManager
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt
from ui.customer_form import CustomerForm  # імпортуємо форму


class CustomersWindow(QDialog):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Клієнти")
        self.resize(900, 450)


        db = DatabaseManager()
        self.conn = db.connect()
        self.cursor = self.conn.cursor()



        # --- Головний layout ---
        main_layout = QVBoxLayout()


        # --- Кнопки ---
        btn_layout = QHBoxLayout()
        self.btn_menu = QPushButton("Меню")
        self.btn_add = QPushButton("Додати")
        self.btn_edit = QPushButton("Редагувати")
        self.btn_delete = QPushButton("Видалити")


        for btn in [self.btn_menu, self.btn_add, self.btn_edit, self.btn_delete]:
            btn_layout.addWidget(btn)


        self.btn_menu.clicked.connect(self.go_to_menu)
        self.btn_add.clicked.connect(self.add_customer)
        self.btn_edit.clicked.connect(self.edit_customer)
        self.btn_delete.clicked.connect(self.delete_customer)


        main_layout.addLayout(btn_layout)


        # --- Таблиця ---
        self.table = QTableWidget()
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)


        self.load_data()


    def load_data(self):
        """Зчитування даних з таблиці Customers"""
        try:
            self.cursor.execute("SELECT id, name, email, phone, address FROM Customers")
            rows = self.cursor.fetchall()
            headers = ["ID", "Прізвище та ім’я", "Email", "Телефон", "Адреса"]


            self.table.setColumnCount(len(headers))
            self.table.setRowCount(len(rows))
            self.table.setHorizontalHeaderLabels(headers)


            for r, row in enumerate(rows):
                for c, val in enumerate(row):
                    item = QTableWidgetItem(str(val))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.table.setItem(r, c, item)


            self.table.hideColumn(0)
            self.table.resizeColumnsToContents()


        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зчитати дані:\n{e}")


    # --- Кнопки ---
    def go_to_menu(self):
        self.close()
        if self.main_window:
            self.main_window.show()


    def add_customer(self):
        form = CustomerForm(mode="add")
        if form.exec_():
            self.load_data()


    def edit_customer(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Увага", "Виберіть клієнта для редагування.")
            return
        customer_data = [
            self.table.item(selected, c).text() for c in range(self.table.columnCount())
        ]
        form = CustomerForm(mode="edit", customer_data=customer_data)
        if form.exec_():
            self.load_data()


    def delete_customer(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Увага", "Виберіть клієнта для видалення.")
            return


        customer_id = self.table.item(selected, 0).text()
        confirm = QMessageBox.question(
            self, "Підтвердження",
            f"Видалити клієнта з ID {customer_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM Customers WHERE id=?", (customer_id,))
                self.conn.commit()
                self.load_data()
                QMessageBox.information(self, "Успіх", "Клієнта видалено.")
            except Exception as e:
                QMessageBox.critical(self, "Помилка", f"Не вдалося видалити:\n{e}")