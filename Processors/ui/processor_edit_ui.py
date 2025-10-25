from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QPushButton, QVBoxLayout
)
from models.database import DatabaseManager


class ProcessorEditDialog(QDialog):
    def __init__(self, processor=None):
        super().__init__()
        self.setWindowTitle("Процесор")
        self.processor = processor  # None для додавання, dict для редагування
        self.db = DatabaseManager()
        self.conn = self.db.connect()
        self.cursor = self.conn.cursor()


        layout = QVBoxLayout()
        form = QFormLayout()


        # Поля
        self.name_edit = QLineEdit()
        self.brand_combo = QComboBox()
        self.series_edit = QLineEdit()
        self.gen_edit = QLineEdit()
        self.cores_spin = QSpinBox(); self.cores_spin.setMaximum(128)
        self.threads_spin = QSpinBox(); self.threads_spin.setMaximum(256)
        self.base_spin = QDoubleSpinBox(); self.base_spin.setDecimals(2); self.base_spin.setMaximum(10)
        self.boost_spin = QDoubleSpinBox(); self.boost_spin.setDecimals(2); self.boost_spin.setMaximum(10)
        self.tdp_spin = QSpinBox(); self.tdp_spin.setMaximum(500)
        self.socket_combo = QComboBox()
        self.year_spin = QSpinBox(); self.year_spin.setRange(1970, 2100)
        self.price_spin = QDoubleSpinBox(); self.price_spin.setDecimals(2); self.price_spin.setMaximum(10000)
        self.stock_spin = QSpinBox(); self.stock_spin.setMaximum(1000)


        # Завантаження брендів
        self.cursor.execute("SELECT id, name FROM Brands")
        self.brands = self.cursor.fetchall()
        for b in self.brands:
            self.brand_combo.addItem(b[1], b[0])


        # Завантаження сокетів
        self.cursor.execute("SELECT id, name FROM Sockets")
        self.sockets = self.cursor.fetchall()
        for s in self.sockets:
            self.socket_combo.addItem(s[1], s[0])


        # Додавання у форму
        form.addRow("Назва:", self.name_edit)
        form.addRow("Бренд:", self.brand_combo)
        form.addRow("Серія:", self.series_edit)
        form.addRow("Покоління:", self.gen_edit)
        form.addRow("Ядра:", self.cores_spin)
        form.addRow("Потоки:", self.threads_spin)
        form.addRow("Баз. частота (ГГц):", self.base_spin)
        form.addRow("Boost (ГГц):", self.boost_spin)
        form.addRow("TDP (Вт):", self.tdp_spin)
        form.addRow("Сокет:", self.socket_combo)
        form.addRow("Рік релізу:", self.year_spin)
        form.addRow("Ціна ($):", self.price_spin)
        form.addRow("Залишок:", self.stock_spin)


        layout.addLayout(form)


        # Кнопка Зберегти
        self.btn_save = QPushButton("Зберегти")
        self.btn_save.clicked.connect(self.save_processor)
        layout.addWidget(self.btn_save)


        self.setLayout(layout)


        # Якщо редагування, заповнюємо дані
        if self.processor:
            self.load_data()


    def load_data(self):
        self.name_edit.setText(self.processor['name'])
        self.series_edit.setText(self.processor['series'])
        self.gen_edit.setText(self.processor['generation'])
        self.cores_spin.setValue(self.processor['cores'])
        self.threads_spin.setValue(self.processor['threads'])
        self.base_spin.setValue(self.processor['base_clock'])
        self.boost_spin.setValue(self.processor['boost_clock'])
        self.tdp_spin.setValue(self.processor['tdp'])
        self.year_spin.setValue(self.processor['release_year'])
        self.price_spin.setValue(self.processor['price_usd'])
        self.stock_spin.setValue(self.processor['stock_quantity'])


        # Встановлення бренду і сокета
        brand_index = self.brand_combo.findData(self.processor['brand_id'])
        if brand_index >= 0:
            self.brand_combo.setCurrentIndex(brand_index)
        socket_index = self.socket_combo.findData(self.processor['socket_id'])
        if socket_index >= 0:
            self.socket_combo.setCurrentIndex(socket_index)


    def save_processor(self):
        name = self.name_edit.text()
        brand_id = self.brand_combo.currentData()
        series = self.series_edit.text()
        generation = self.gen_edit.text()
        cores = self.cores_spin.value()
        threads = self.threads_spin.value()
        base_clock = self.base_spin.value()
        boost_clock = self.boost_spin.value()
        tdp = self.tdp_spin.value()
        socket_id = self.socket_combo.currentData()
        release_year = self.year_spin.value()
        price = self.price_spin.value()
        stock = self.stock_spin.value()


        if self.processor:  # редагування
            self.cursor.execute("""
                UPDATE Processors SET name=?, brand_id=?, series=?, generation=?,
                cores=?, threads=?, base_clock=?, boost_clock=?, tdp=?,
                socket_id=?, release_year=?, price_usd=?, stock_quantity=?
                WHERE id=?
            """, (name, brand_id, series, generation, cores, threads, base_clock, boost_clock,
                  tdp, socket_id, release_year, price, stock, self.processor['id']))
        else:  # додати
            self.cursor.execute("""
                INSERT INTO Processors 
                (name, brand_id, series, generation, cores, threads, base_clock, boost_clock,
                tdp, socket_id, release_year, price_usd, stock_quantity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, brand_id, series, generation, cores, threads, base_clock, boost_clock,
                  tdp, socket_id, release_year, price, stock))


        self.conn.commit()
        self.conn.close()
        self.accept()  # закриває діалог
