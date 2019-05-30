from label import LabelTool
import sys
from label_tool_ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QPushButton, QMainWindow


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pb_half_full_label.clicked.connect(self.analysis_half_full_label_click)
        self.ui.pb_mono_label.clicked.connect(self.analysis_mono_label_click)

    def analysis_half_full_label_click(self):
        message = LabelTool.analysis_label(is_half_full=True)
        QMessageBox.information(self,
                                '>_<',
                                message,
                                QMessageBox.Yes)

    def analysis_mono_label_click(self):
        message = LabelTool.analysis_label(is_mono=True)
        QMessageBox.information(self,
                                '>_<',
                                message,
                                QMessageBox.Yes)


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())

