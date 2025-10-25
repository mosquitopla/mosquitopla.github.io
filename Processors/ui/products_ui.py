from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QMessageBox, QComboBox, QLabel, QLineEdit
)
from PyQt5.QtCore import Qt
from models.database import DatabaseManager
from .processor_details_ui import ProcessorDetailsWindow
from .processor_edit_ui import ProcessorEditDialog

class ProductsWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Процесори")
        self.setGeometry(350, 200, 1000, 400)

        layout = QVBoxLayout()

        btn_layout = QHBoxLayout()
        self.back_btn = QPushButton("⬅ Меню")
        self.btn_add = QPushButton("Додати")
        self.btn_edit = QPushButton("Редагувати")
        self.btn_delete = QPushButton("Видалити")
        self.btn_details = QPushButton("Деталі")
        btn_layout.addWidget(self.back_btn)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_details)
        layout.addLayout(btn_layout)

        sort_layout = QHBoxLayout()
        self.sort_field = QComboBox()
        self.sort_field.addItems(["Назва", "Бренд", "Ядра", "Потоки", "Ціна ($)", "Залишок"])
        self.sort_order = QComboBox()
        self.sort_order.addItems(["За зростанням", "За спаданням"])


        sort_layout.addWidget(QLabel("Сортування:"))
        sort_layout.addWidget(self.sort_field)
        sort_layout.addWidget(self.sort_order)
        sort_layout.addStretch()
        layout.addLayout(sort_layout)


        # --- Фільтрування ---
        filter_layout = QHBoxLayout()
        self.filter_field = QComboBox()
        self.filter_field.addItems(["Назва", "Бренд", "Ядра", "Потоки", "Ціна ($)", "Залишок"])


        self.filter_input1 = QLineEdit()
        self.filter_input2 = QLineEdit()
        self.filter_input1.setPlaceholderText("Від...")
        self.filter_input2.setPlaceholderText("До...")


        self.btn_apply_filter = QPushButton("🔍 Застосувати")
        self.btn_clear_filter = QPushButton("✖ Очистити")


        for btn in [self.btn_apply_filter, self.btn_clear_filter]:
            btn.setFixedWidth(100)


        filter_layout.addWidget(QLabel("Фільтр:"))
        filter_layout.addWidget(self.filter_field)
        filter_layout.addWidget(self.filter_input1)
        filter_layout.addWidget(self.filter_input2)
        filter_layout.addWidget(self.btn_apply_filter)
        filter_layout.addWidget(self.btn_clear_filter)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)


        # Таблиця
        self.table = QTableWidget()
        layout.addWidget(self.table)


        self.setLayout(layout)


        # Підключення кнопок
        self.back_btn.clicked.connect(self.go_back)
        self.btn_add.clicked.connect(self.add_processor)
        self.btn_edit.clicked.connect(self.edit_processor)
        self.btn_delete.clicked.connect(self.delete_processor)
        self.btn_details.clicked.connect(self.show_details)


        self.sort_field.currentIndexChanged.connect(self.sort_table)
        self.sort_order.currentIndexChanged.connect(self.sort_table)
        self.btn_apply_filter.clicked.connect(self.apply_filter)
        self.btn_clear_filter.clicked.connect(self.clear_filter)


        # --- Дані ---
        self.all_rows = []
        self.load_data()


    def go_back(self):
        self.close()
        self.main_window.show()

    def load_data(self):
        db = DatabaseManager()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.name, b.name AS brand, p.cores, p.threads, p.price_usd, p.stock_quantity
            FROM Processors p
            LEFT JOIN Brands b ON p.brand_id = b.id
        """)
        rows = cursor.fetchall()
        conn.close()
        
        cleaned_rows = []
        for row in rows:
            row = list(row)
            for i in (3, 4, 5, 6):  # ядра, потоки, ціна, залишок
                try:
                    row[i] = float(row[i])
                except (TypeError, ValueError):
                    row[i] = 0.0
            cleaned_rows.append(tuple(row))


        self.all_rows = cleaned_rows
        self.current_rows = list(self.all_rows)
        self.display_data(self.current_rows)

        

    def display_data(self, rows):
        headers = ["ID", "Назва", "Бренд", "Ядра", "Потоки", "Ціна ($)", "Залишок"]
        self.table.setSortingEnabled(False)
        self.table.clearContents()
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.hideColumn(0)
        self.table.setColumnWidth(1, 300)


        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value) if value is not None else "")
                # числові поля — 3, 4, 5, 6
                if col_idx in (3, 4, 5, 6):
                    try:
                        item.setData(Qt.EditRole, float(value))
                    except (TypeError, ValueError):
                        item.setData(Qt.EditRole, 0.0)
                self.table.setItem(row_idx, col_idx, item)


        self.table.setSortingEnabled(False)


    def show_details(self):
        sel = self.table.currentRow()
        if sel == -1:
            QMessageBox.warning(self, "Помилка", "Оберіть рядок")
            return
        proc_id = int(self.table.item(sel, 0).text())
        db = DatabaseManager()
        conn = db.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id, p.name, b.name AS brand, p.series, p.generation, p.cores,
                   p.threads, p.base_clock, p.boost_clock, p.tdp,
                   s.name AS socket, p.release_year, p.price_usd, p.stock_quantity
            FROM Processors p
            LEFT JOIN Brands b ON p.brand_id = b.id
            LEFT JOIN Sockets s ON p.socket_id = s.id
            WHERE p.id=?
        """, (proc_id,))
        details = cur.fetchone()
        conn.close()
        if details:
            self.details_window = ProcessorDetailsWindow(details)
            self.details_window.show()

    def add_processor(self):
        dialog = ProcessorEditDialog()
        if dialog.exec_():
            self.load_data()

    def edit_processor(self):
        sel = self.table.currentRow()
        if sel == -1:
            QMessageBox.warning(self, "Помилка", "Оберіть процесор для редагування")
            return
        proc_id = int(self.table.item(sel, 0).text())
        
        db = DatabaseManager()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, brand_id, series, generation, cores, threads, base_clock, boost_clock, tdp, socket_id, release_year, price_usd, stock_quantity
            FROM Processors WHERE id=?
        """, (proc_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            proc = {
                'id': row[0], 'name': row[1], 'brand_id': row[2], 'series': row[3],
                'generation': row[4], 'cores': row[5], 'threads': row[6],
                'base_clock': row[7], 'boost_clock': row[8], 'tdp': row[9],
                'socket_id': row[10], 'release_year': row[11], 'price_usd': row[12],
                'stock_quantity': row[13]
            }
            dialog = ProcessorEditDialog(proc)
            if dialog.exec_():
                self.load_data()

    def delete_processor(self):
        sel = self.table.currentRow()
        if sel == -1:
            QMessageBox.warning(self, "Помилка", "Оберіть процесор для видалення")
            return
        proc_id = int(self.table.item(sel, 0).text())
        reply = QMessageBox.question(self, "Підтвердити", f"Видалити процесор ID {proc_id}?", QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.Yes:
            db = DatabaseManager()
            conn = db.connect()
            cur = conn.cursor()
            cur.execute("DELETE FROM Processors WHERE id=?", (proc_id,))
            conn.commit()
            conn.close()
            self.load_data()

    def sort_table(self):
        field_map = {
            "Назва": (1, 'str'),
            "Бренд": (2, 'str'),
            "Ядра": (3, 'num'),
            "Потоки": (4, 'num'),
            "Ціна ($)": (5, 'num'),
            "Залишок": (6, 'num')
        }


        key_name = self.sort_field.currentText()
        col_idx, typ = field_map[key_name]
        ascending = self.sort_order.currentText() == "За зростанням"


        def key_func(row):
            val = row[col_idx]
            if typ == 'num':
                try:
                    return float(val)
                except (TypeError, ValueError):
                    return float('-inf')
            else:
                return str(val).lower() if val else ""


        self.current_rows.sort(key=key_func, reverse=not ascending)
        self.display_data(self.current_rows)


    def apply_filter(self):
        field = self.filter_field.currentText()
        val1 = self.filter_input1.text().strip()
        val2 = self.filter_input2.text().strip()


        filtered = []
        for row in self.all_rows:
            name, brand, cores, threads, price, stock = row[1], row[2], row[3], row[4], row[5], row[6]


            if field in ["Назва", "Бренд"]:
                text_val = val1.lower()
                if text_val in (name.lower() if field == "Назва" else brand.lower()):
                    filtered.append(row)
            else:
                try:
                    v1 = float(val1) if val1 else None
                    v2 = float(val2) if val2 else None
                    num = {
                        "Ядра": cores,
                        "Потоки": threads,
                        "Ціна ($)": price,
                        "Залишок": stock
                    }[field]
                    if (v1 is None or num >= v1) and (v2 is None or num <= v2):
                        filtered.append(row)
                except ValueError:
                    continue


        self.display_data(filtered)


    def clear_filter(self):
        self.filter_input1.clear()
        self.filter_input2.clear()
        self.display_data(self.all_rows)
