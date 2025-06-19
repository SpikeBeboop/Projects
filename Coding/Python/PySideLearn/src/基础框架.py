from PySide6.QtWidgets import QApplication, QMainWindow,QPushButton

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        btn = QPushButton("新按钮",self)
        btn.setGeometry(0,0,200,100)
        btn.setToolTip('按钮提示')
        btn.setText('重新设置')

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()