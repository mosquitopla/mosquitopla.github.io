from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTableWidget, QTableWidgetItem,
    QPushButton, QSpinBox, QMessageBox
)
from PyQt5.QtCore import Qt
from datetime import datetime
from models.database import DatabaseManager  # імпорт singleton


class OrderForm(QWidget):
    def __init__(self, parent_window, order_id=None):
        super().__init__()
        self.parent_window = parent_window
        self.order_id = order_id
        self.setWindowTitle("Редагування замовлення" if order_id else "Нове замовлення")
        self.resize(850, 550)


        # Підключення до бази через singleton
        db = DatabaseManager()
        self.conn = db.connect()
        self.cursor = self.conn.cursor()


        # --- Основний layout ---
        layout = QVBoxLayout()


        # --- Вибір покупця ---
        customer_layout = QHBoxLayout()
        customer_layout.addWidget(QLabel("Покупець:"))
        self.cmb_customer = QComboBox()
        customer_layout.addWidget(self.cmb_customer)
        layout.addLayout(customer_layout)


        # --- Статус замовлення ---
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Статус:"))
        self.cmb_status = QComboBox()
        status_layout.addWidget(self.cmb_status)
        layout.addLayout(status_layout)


        if not self.order_id:
            self.cmb_status.addItem("Нове")
            self.cmb_status.setEnabled(False)
        else:
            self.cmb_status.addItems(["Оплачено", "Видано"])


        # --- Таблиця з процесорами ---
        layout.addWidget(QLabel("Виберіть процесори:"))
        self.table = QTableWidget()
        layout.addWidget(self.table)


        # --- Кнопки ---
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("💾 Зберегти")
        self.btn_cancel = QPushButton("❌ Скасувати")
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)


        self.setLayout(layout)


        # Події кнопок
        self.btn_save.clicked.connect(self.save_order)
        self.btn_cancel.clicked.connect(self.cancel)


        # Завантаження даних
        self.load_customers()
        self.load_processors()


        if self.order_id:
            self.load_order_data()


    # -------------------- Завантаження --------------------


    def load_customers(self):
        """Завантажити список покупців."""
        self.cursor.execute("SELECT id, name FROM Customers")
        customers = self.cursor.fetchall()
        for cid, name in customers:
            self.cmb_customer.addItem(name, cid)


    def load_processors(self):
        """Завантажити процесори."""
        self.cursor.execute("SELECT id, name, price_usd, stock_quantity FROM Processors")
        rows = self.cursor.fetchall()


        headers = ["ID", "Назва процесора", "Ціна ($)", "Залишок (шт)", "Кількість"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(rows))


        for i, (pid, name, price, stock) in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(pid)))
            self.table.setItem(i, 1, QTableWidgetItem(name))
            self.table.setItem(i, 2, QTableWidgetItem(f"{price:.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(str(stock)))


            spin = QSpinBox()
            spin.setRange(0, stock if stock is not None else 0)
            self.table.setCellWidget(i, 4, spin)


        self.table.hideColumn(0)
        self.table.resizeColumnsToContents()


    def load_order_data(self):
        """Завантаження даних замовлення для редагування."""
        self.cursor.execute("SELECT customer_id, status FROM Orders WHERE id=?", (self.order_id,))
        order = self.cursor.fetchone()
        if order:
            customer_id, status = order
            idx = self.cmb_customer.findData(customer_id)
            if idx >= 0:
                self.cmb_customer.setCurrentIndex(idx)


            if status in ["Оплачено", "Видано"]:
                self.cmb_status.setCurrentText(status)


        # Позиції замовлення
        self.cursor.execute("SELECT processor_id, quantity FROM OrderItems WHERE order_id=?", (self.order_id,))
        items = dict(self.cursor.fetchall())


        for i in range(self.table.rowCount()):
            pid = int(self.table.item(i, 0).text())
            if pid in items:
                spin = self.table.cellWidget(i, 4)
                spin.setValue(items[pid])


    # -------------------- Збереження --------------------


    def save_order(self):
        """Зберегти замовлення (нове або відредаговане)."""
        customer_id = self.cmb_customer.currentData()
        if customer_id is None:
            QMessageBox.warning(self, "Помилка", "Оберіть покупця!")
            return


        db = DatabaseManager()
        conn = db.connect()
        cursor = conn.cursor()


        order_date = datetime.now().strftime("%Y-%m-%d")


        # --- визначаємо старий та новий статус ---
        if self.order_id:
            new_status = self.cmb_status.currentText() or "Нове"
            cursor.execute("SELECT status FROM Orders WHERE id=?", (self.order_id,))
            old_status = cursor.fetchone()
            old_status = old_status[0] if old_status else None
        else:
            new_status = "Нове"
            old_status = None


        order_items = []
        total = 0.0


        # --- зібрати вибрані товари ---
        for i in range(self.table.rowCount()):
            pid_item = self.table.item(i, 0)
            price_item = self.table.item(i, 2)
            if pid_item is None or price_item is None:
                continue


            pid = int(pid_item.text())
            price = float(price_item.text())
            spin = self.table.cellWidget(i, 4)
            qty = spin.value() if spin else 0


            if qty > 0:
                subtotal = price * qty
                total += subtotal
                order_items.append((pid, qty, price, subtotal))


        if not order_items:
            QMessageBox.warning(self, "Помилка", "Оберіть хоча б один процесор!")
            return


        try:
            # --- оновлення або створення замовлення ---
            if self.order_id:
                cursor.execute(
                    "UPDATE Orders SET customer_id=?, total_price=?, status=? WHERE id=?",
                    (customer_id, total, new_status, self.order_id)
                )
                cursor.execute("DELETE FROM OrderItems WHERE order_id=?", (self.order_id,))
                order_id = self.order_id
            else:
                cursor.execute(
                    "INSERT INTO Orders (customer_id, order_date, status, total_price) VALUES (?, ?, ?, ?)",
                    (customer_id, order_date, new_status, total)
                )
                order_id = cursor.lastrowid


            # --- вставка позицій ---
            for pid, qty, price, subtotal in order_items:
                cursor.execute("""
                    INSERT INTO OrderItems (order_id, processor_id, quantity, unit_price, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                """, (order_id, pid, qty, price, subtotal))


            # --- якщо статус змінено з "Нове" → "Оплачено" ---
            if old_status == "Нове" and new_status == "Оплачено":
                for pid, qty, _, _ in order_items:
                    cursor.execute("""
                        UPDATE Processors
                        SET stock_quantity = stock_quantity - ?
                        WHERE id = ? AND stock_quantity >= ?
                    """, (qty, pid, qty))


            conn.commit()
            QMessageBox.information(self, "Успіх", "Замовлення збережено успішно!")
            self.close()
            self.parent_window.load_data()
            self.parent_window.show()


        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти замовлення:\n{e}")


    # -------------------- Інші методи --------------------


    def cancel(self):
        self.close()
        self.parent_window.show()


    def closeEvent(self, event):
        self.conn.close()
        super().closeEvent(event)
