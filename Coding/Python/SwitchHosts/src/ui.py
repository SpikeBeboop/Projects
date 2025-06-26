from PySide6.QtWidgets import (
    QMainWindow, QWidget
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SwitchHosts")
        self.resize(800, 600)