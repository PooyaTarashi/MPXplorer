from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFormLayout, QGroupBox, QScrollArea, QVBoxLayout
from collections import OrderedDict
from time import sleep
import sys
import os

class PPushButton(QPushButton):
    def __init__(self, parent, id, path:str):
        super().__init__(parent)
        self.id = id
        self.clicked.connect(lambda: self.init_page(parent, path))
        # print(parent)


    def init_page(self, parent, path):
        parent.initialize_page(path)

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Welcome to MPXplorer")
        self.icons_btn = []
        self.icons_lbl = []
        self.lines = []
        self.paths = []
        self.setGeometry(500, 200, 1050, 700)
        self.setWindowTitle("MPXplorer")
        self.initialize_page()
        

    def initialize_page(self, default_dir = "C:\\Users\\Dell\\Desktop\\tesktop"):
        self.icons_btn = []
        self.icons_lbl = []
        self.lines = []
        self.paths = []
        self.clear_screen()
        
        wid = QWidget(self)
        self.setCentralWidget(wid)

        form_layout = QFormLayout()
        group_box = QGroupBox(default_dir)

        

        cnt = 0
        for itm in get_data(default_dir).values():
            btn = PPushButton(self, id=cnt, path=itm.path)
            lbl = QLabel(itm.name, self)
            btn.setText(itm.name)
            btn.setFixedSize(800, 70)
            lbl.setFixedSize(200, 20)
            
            self.icons_btn.append(btn)
            self.icons_lbl.append(lbl)
            form_layout.addRow(self.icons_lbl[cnt], self.icons_btn[cnt])
            self.lines.append(QLabel('_______________________________________________________________________________________________________________________________________________'))
            form_layout.addRow(self.lines[cnt])
            cnt += 1
            
        exit_btn = QPushButton("Exit", self)
        exit_btn.clicked.connect(self.clear_screen)
        form_layout.addRow(exit_btn)

        group_box.setLayout(form_layout)
        scroll = QScrollArea()
        scroll.setWidget(group_box)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(700)
        scroll.setFixedWidth(1060)

        layout = QVBoxLayout()
        layout.addWidget(scroll)

        wid.setLayout(layout)
        
        self.show()

        
    def clear_screen(self):
        for itm in self.icons_lbl:
            itm.clear()
        for itm in self.lines:
            itm.clear()



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