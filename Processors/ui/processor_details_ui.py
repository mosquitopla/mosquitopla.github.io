from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem


class ProcessorDetailsWindow(QWidget):
    def __init__(self, details):
        super().__init__()
        self.setWindowTitle(f"Деталі процесора: {details[1]}")
        self.setGeometry(350, 250, 500, 400)


        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)


        self.load_details(details)


    def load_details(self, details):
        # Заголовки: характеристика - значення
        labels = [
            "ID", "Назва", "Бренд", "Серія", "Покоління",
            "Ядра", "Потоки", "Баз. частота (ГГц)", "Boost (ГГц)",
            "TDP (Вт)", "Сокет", "Рік релізу", "Ціна ($)", "Залишок"
        ]


        self.table.setRowCount(len(labels))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Характеристика", "Значення"])


        for i, label in enumerate(labels):
            self.table.setItem(i, 0, QTableWidgetItem(label))
            self.table.setItem(i, 1, QTableWidgetItem(str(details[i])))


        self.table.resizeColumnsToContents()
