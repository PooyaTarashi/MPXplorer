from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QLabel, QFormLayout, QGroupBox, QScrollArea, QVBoxLayout
from collections import OrderedDict
from time import sleep
import sys
import subprocess
import os

class PPushButton(QPushButton):
    """
    A customized PyQt QPushButton class that accepts a FileExplorer object, a button id, and a directory path as arguments.

    Args:
    parent: An instance of the FileExplorer class that is used to access files and directories.
    button_id (int or str): A unique identifier for the button.
    dir_path (str): The directory path that the button will be associated with.

    Attributes:
    button_id (int or str): A unique identifier for the button.

    Methods:
    No additional methods attached to this class other than inherited QPushButton methods. However, the properties above can be accessed publicly by using the appropriate function calls within the PPushButton object.

    """
    def __init__(self, parent, id, item:str):
        super().__init__(parent)
        self.id = id
        if item.is_dir:
            self.clicked.connect(lambda: parent.initialize_page(item.path))
        else:
            self.clicked.connect(lambda: subprocess.Popen(item.path, shell=True))



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


        exit_btn = QPushButton("Exit", self)    # Add exit button.
        exit_btn.clicked.connect(sys.exit)
        form_layout.addRow(exit_btn)

        cnt = 0
        for itm in get_data(default_dir).values():    # iterates values of Item objects in the specified directory and makes button and label for each object.
            btn = PPushButton(self, id=cnt, item=itm)    # Make object of PPushButton customized class.
            lbl = QLabel(itm.name, self)
            btn.setText(itm.name)
            btn.setFixedSize(800, 70)
            lbl.setFixedSize(200, 20)
            
            # Stores button and label data:
            self.icons_btn.append(btn)
            self.icons_lbl.append(lbl)
            form_layout.addRow(self.icons_lbl[cnt], self.icons_btn[cnt])    # Add a row to form_layout.
            self.lines.append(QLabel('_______________________________________________________________________________________________________________________________________________'))    # Draws a vertical line.
            form_layout.addRow(self.lines[cnt])
            cnt += 1
            

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
        dir_contents_dict[itm.name] = Item(itm.name, itm.path, itm.is_dir())
    return dir_contents_dict



if __name__ == "__main__":
    app = QApplication(sys.argv)
    MPXplorer = FileExplorer()
    sys.exit(app.exec_())