from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFormLayout, QGroupBox
from collections import OrderedDict
import sys
import os

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Welcome to MPXplorer")

        default_dir = "C:\\Users\\Dell\\Desktop\\tesktop"
        self.setGeometry(460, 240, 710, 500)
        self.setWindowTitle("MPXplorer")
        
        form_layout = QFormLayout()
        group_box = QGroupBox('GroupBox')

        
        btn_y_idx = 0
        btn_x_idx = 0
        lbl_y_idx = 1
        lbl_x_idx = 0

        icons_btn = []
        icons_lbl = []
        for itm in get_data(default_dir).values():  # this loop makes buttons with text value of directory name.
            btn = QtWidgets.QPushButton(self)
            lbl = QLabel(itm.name, self)
            lbl.move(lbl_x_idx * 150, lbl_y_idx * 150 - 35)
            btn.setText(itm.name)
            btn.move(btn_x_idx * 150, btn_y_idx * 150 + 20)
            btn.setFixedSize(90, 100)
            icons_btn.append(btn)
            icons_lbl.append(lbl)
            btn_x_idx += 1
            lbl_x_idx += 1
            if btn_x_idx % 5 == 0:
                btn_y_idx += 1
                btn_x_idx %= 5
            if lbl_x_idx % 5 == 0:
                lbl_y_idx += 1
                lbl_x_idx %= 5
        self.show()



class Item():
    def __init__(self, name, path, is_dir):
        self.name = name
        self.path = path
        self.is_dir = is_dir


def get_data(directory_path = "C:\\Users\\Dell\\Desktop\\tesktop"):
    dir_contents_ls = os.scandir(directory_path)
    dir_contents_dict = OrderedDict()
    for itm in dir_contents_ls:
        dir_contents_dict[itm.name] = Item(itm.name, itm.path, itm.is_dir)
    return dir_contents_dict



if __name__ == "__main__":
    app = QApplication(sys.argv)
    MPXplorer = FileExplorer()
    sys.exit(app.exec_())