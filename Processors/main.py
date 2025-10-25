import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
        
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())
