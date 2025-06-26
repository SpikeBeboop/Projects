import sys

from PySide6.QtWidgets import QApplication
from ui import CalcUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalcUI()
    window.show()
    sys.exit(app.exec())
