import sys
from PyQt5.QtWidgets import QApplication,QWidget, QDialog
from firstwindow import Ui_Dialog

class firstWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = UI_Dialog()
        self.ui.setupUi(self)
        self.show()

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
