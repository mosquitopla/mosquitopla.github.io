import sqlite3
from models.database import DatabaseManager
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt


class OrderDetailsWindow(QWidget):
    def __init__(self, order_id, main_window=None):
        super().__init__()
        self.order_id = order_id
        self.main_window = main_window
        self.setWindowTitle(f"Деталі замовлення №{order_id}")
        self.resize(800, 400)


        # Підключення до БД
        db = DatabaseManager()
        self.conn = db.connect()
        self.cursor = self.conn.cursor()



        # --- Основний layout ---
        layout = QVBoxLayout()


        # --- Верхня панель ---
        header_layout = QHBoxLayout()
        self.label_title = QLabel(f"<b>Замовлення №{order_id}</b>")
        self.btn_back = QPushButton("⬅ Назад")
        self.btn_back.setFixedWidth(120)
        self.btn_back.clicked.connect(self.go_back)
        header_layout.addWidget(self.label_title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_back)
        layout.addLayout(header_layout)


        # --- Таблиця з деталями ---
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)


        # --- Завантаження даних ---
        self.load_details()


    def go_back(self):
        """Повернення у вікно замовлень."""
        self.close()
        if self.main_window:
            self.main_window.show()


    def load_details(self):
        """Завантажуємо позиції замовлення."""
        try:
            self.cursor.execute("""
                SELECT 
                    p.name AS processor_name,
                    oi.quantity,
                    oi.unit_price,
                    oi.subtotal
                FROM OrderItems oi
                LEFT JOIN Processors p ON oi.processor_id = p.id
                WHERE oi.order_id = ?
            """, (self.order_id,))
            rows = self.cursor.fetchall()


            headers = ["Процесор", "Кількість", "Ціна за одиницю ($)", "Сума ($)"]
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            self.table.setRowCount(len(rows))


            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value) if value is not None else "")
                    if col_idx in [1, 2, 3]:
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.table.setItem(row_idx, col_idx, item)


            self.table.resizeColumnsToContents()


            # якщо замовлення пусте
            if not rows:
                QMessageBox.information(self, "Інформація", "Це замовлення не містить товарів.")


        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зчитати деталі замовлення:\n{e}")


    def closeEvent(self, event):
        """Закриваємо з’єднання з БД."""
        self.conn.close()
        super().closeEvent(event)
