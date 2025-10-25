import sys
import random
from PyQt5.QtWidgets import QApplication,QHBoxLayout, QMessageBox, QLineEdit, QWidget, QVBoxLayout,QLabel, QListWidget, QPushButton
from PyQt5.QtCore import Qt

class WinnerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Визначення переможця")
        self.setGeometry(500, 300, 400, 300)
        # --- Основне розміщення ---
        main_layout = QVBoxLayout()


        # Заголовок
        self.label = QLabel("Введіть імена учасників або виберіть зі списку")
        self.label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label)

        # ... усередині конструктора класу:  
        self.user_list = QListWidget()
        main_layout.addWidget(self.user_list)

        input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введіть ім'я учасника")


        self.add_btn = QPushButton("Додати")
        self.add_btn.clicked.connect(self.add_user)
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.add_btn)

        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)

        btn_layout = QHBoxLayout()

        
        self.pick_btn = QPushButton("Обрати переможця")
        self.pick_btn.clicked.connect(self.pick_winner)
        
        self.clear_btn = QPushButton("🧹 Очистити список")
        self.clear_btn.clicked.connect(self.clear_list)
        
        self.save_btn = QPushButton("💾 Зберегти")
        self.save_btn.clicked.connect(self.save_users)

        
        main_layout.addWidget(self.pick_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.save_btn)
        main_layout.addLayout(btn_layout)

        
        # Виведення результату
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size: 18px; color: green; font-weight: bold;")
        self.result_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.result_label)
        
        self.load_users()
        
    def add_user(self):     
        name = self.name_input.text().strip()
        if name:
            self.user_list.addItem(name)
            self.name_input.clear()
        else:
            QMessageBox.warning(self, "Помилка", "Введіть ім'я учасника!")


    def pick_winner(self):
        """Випадково вибирає переможця"""
        count = self.user_list.count()
        if count == 0:
            QMessageBox.warning(self, "Помилка", "Список учасників порожній!")
            return


        users = [self.user_list.item(i).text() for i in range(count)]
        winner = random.choice(users)
        self.result_label.setText(f"🎉 Переможець: {winner}!")
        QMessageBox.information(self, "Результат", f"🎉 Переможець: {winner}!")

        
    def clear_list(self):
        if self.user_list.count() == 0:
            QMessageBox.information(self, "Інформація", "Список уже порожній.")
            return


        reply = QMessageBox.question(
            self, "Підтвердження", "Ви дійсно хочете очистити список?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.user_list.clear()
            self.result_label.clear()
            QMessageBox.information(self, "Очищено", "Список успішно очищено!")

    
    def save_users(self):
        users = [self.user_list.item(i).text() for i in range(self.user_list.count())]
        with open("users.txt", "w", encoding="utf-8") as f:
            for name in users:
                f.write(name + "\n")
        QMessageBox.information(self, "Збережено", "Список учасників успішно збережено!")


    # --- Зчитування учасників при запуску ---
    def load_users(self):
        try:
            with open("users.txt", "r", encoding="utf-8") as f:
                for line in f:
                    name = line.strip()
                    if name:
                        self.user_list.addItem(name)
        except FileNotFoundError:
            pass


    # --- Збереження при закритті ---
    def closeEvent(self, event):
        self.save_users()
        event.accept()


app = QApplication(sys.argv)
window = WinnerApp()
window.show()
sys.exit(app.exec_())