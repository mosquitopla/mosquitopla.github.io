import sqlite3
from models.database import DatabaseManager
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)


class CustomerForm(QDialog):
    def __init__(self, mode="add", customer_data=None, db_path="processors.db"):
        """
        mode: 'add' або 'edit'
        customer_data: кортеж (id, name, email, phone, address) при редагуванні
        """
        super().__init__()
        self.mode = mode
        self.customer_data = customer_data
        self.db_path = db_path


        self.setWindowTitle("Редагування клієнта" if mode == "edit" else "Додавання клієнта")
        self.setFixedSize(400, 300)


        db = DatabaseManager()
        self.conn = db.connect()
        self.cursor = self.conn.cursor()



        # --- Поля вводу ---
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()


        form_layout.addRow("Прізвище та ім’я:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Телефон:", self.phone_input)
        form_layout.addRow("Адреса:", self.address_input)


        # --- Кнопки ---
        button_layout = QHBoxLayout()
        self.btn_save = QPushButton("Зберегти")
        self.btn_cancel = QPushButton("Скасувати")


        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)


        # --- Основне розташування ---
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)


        # Події
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.save_customer)


        # Якщо режим редагування — заповнити поля
        if self.mode == "edit" and self.customer_data:
            self.load_customer_data()


    def load_customer_data(self):
        """Заповнення полів даними користувача"""
        _, name, email, phone, address = self.customer_data
        self.name_input.setText(name)
        self.email_input.setText(email)
        self.phone_input.setText(phone)
        self.address_input.setText(address)


    def save_customer(self):
        """Додавання або оновлення даних користувача"""
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.text().strip()


        if not name:
            QMessageBox.warning(self, "Помилка", "Поле 'Прізвище та ім’я' є обов’язковим!")
            return


        try:
            if self.mode == "add":
                self.cursor.execute(
                    "INSERT INTO Customers (name, email, phone, address) VALUES (?, ?, ?, ?)",
                    (name, email, phone, address)
                )
            else:
                self.cursor.execute(
                    "UPDATE Customers SET name=?, email=?, phone=?, address=? WHERE id=?",
                    (name, email, phone, address, self.customer_data[0])
                )


            self.conn.commit()
            QMessageBox.information(self, "Успіх", "Дані успішно збережено!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Помилка при збереженні:\n{e}")
        finally:
            self.conn.close()
