from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QLabel, QFormLayout, QGroupBox, QScrollArea, QVBoxLayout, QLineEdit, QCheckBox, QMessageBox
from collections import OrderedDict
from time import sleep
import sys
import subprocess
import os
# from nff import start_dialogue

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
            self.clicked.connect(lambda: parent.open_folder(parent, item))
        else:
            self.clicked.connect(lambda: subprocess.Popen(item.path, shell=True))



class FileExplorer(QMainWindow):
    
    def __init__(self):
        super().__init__()
        print("Welcome to MPXplorer")
        self.icons_btn = []
        self.icons_lbl = []
        self.lines = []
        # self.path_history = []
        self.setGeometry(500, 180, 1050, 800)
        self.setWindowTitle("MPXplorer")
        self.initialize_page()
        

    def initialize_page(self, default_dir = "C:\\Users\\Dell\\Desktop\\tesktop", msg=""):
        self.icons_btn = []
        self.icons_lbl = []
        self.lines = []
        self.lbls_ls = []
        # self.path_history.append(default_dir)
        self.previous_dir = '\\'.join(default_dir.split('\\')[:len(default_dir.split('\\')) - 1])
        print(self.previous_dir)
        self.clear_screen()


        # This label shows messages ==========================================================
        self.my_lbl = QLabel(self)
        self.my_lbl.setText('')
        self.my_lbl.setFixedWidth(500)
        self.my_lbl.move(800, 750)
        if msg == 'T':
            self.my_lbl.setText("Directory has been successfully created.")
            self.my_lbl.setStyleSheet('color: green')
        elif msg == 'F':
            self.my_lbl.setText("Something went wrong, check the folder name.")
            self.my_lbl.setStyleSheet('color: red')
        self.lbls_ls.append(self.my_lbl)
        self.my_lbl.show()
        # ===================================================================================

        # This label shows how many items are in each page ==================================
        self.status_lbl = QLabel("{} items found.".format(len(get_data(default_dir))), self)
        self.status_lbl.setFixedWidth(500)
        self.status_lbl.move(15, 750)
        self.lbls_ls.append(self.status_lbl)
        self.status_lbl.show()
        # ===================================================================================

        wid = QWidget(self)
        self.setCentralWidget(wid)

        form_layout = QFormLayout()
        group_box = QGroupBox(default_dir)



        self.new_btn = QPushButton("+", self)    # Add new file or folder button.
        self.new_btn.setFixedWidth(100)
        self.new_btn.move(840, 15)
        self.new_btn.clicked.connect(lambda: self.new_file_or_folder(default_dir))
        self.new_btn.show()
        
        self.file_name_txt = QLineEdit(self)    # Textbox to get file name
        self.file_name_txt.setFixedWidth(600)
        self.file_name_txt.move(235, 15)
        self.file_name_txt.show()


        # Label to get new file or folder name
        inp_lbl = QLabel("Input file or folder name:", self)
        inp_lbl.setFixedWidth(200)
        inp_lbl.move(85, 15)

        # Checkbox to check whether the new item is file or a directory
        self.is_directory_chckbx = QCheckBox('new directory', self)
        self.is_directory_chckbx.setFixedWidth(300)
        self.is_directory_chckbx.move(950, 15)
        self.is_directory_chckbx.show()

        # add back button to reach previous directory
        self.back_button = QPushButton("<", self)
        self.back_button.clicked.connect(lambda: self.initialize_page(self.previous_dir))
        self.back_button.setFixedWidth(50)
        self.back_button.move(10, 15)

        # add vertical seperator
        self.vrtical_sep = QLabel('|', self)
        self.vrtical_sep.move(70, 15)


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
        scroll.setFixedSize(1060, 700)

        layout = QVBoxLayout()
        layout.addWidget(scroll)

        wid.setLayout(layout)
        
        self.show()


    def clear_screen(self):
        for itm in self.icons_lbl:
            itm.clear()
        for itm in self.lines:
            itm.clear()
        # self.my_lbl.clear()
        for itm in self.lbls_ls:
            itm.clear()

    def open_folder(self, parent, item):
        for itm in parent.lbls_ls:
            itm.clear()
        parent.initialize_page(item.path)

    def new_file_or_folder(self, directory_address):
        state = 'T'
        if self.is_directory_chckbx.isChecked():
            try:
                os.mkdir(directory_address + '\\' + self.file_name_txt.text())
            except:
                state = 'F'
                
        else:
            try:
                f = open(directory_address + '\\' + self.file_name_txt.text(), 'w')
                f.close()
            except:
                state = 'F'

            # subprocess.Popen('cd ' + directory_address + '\n' + 'type nul > ' + self.file_name_txt.text(), shell=True)

        self.is_directory_chckbx.deleteLater()
        self.status_lbl.clear()
        self.my_lbl.clear()
        self.initialize_page(msg=state)



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