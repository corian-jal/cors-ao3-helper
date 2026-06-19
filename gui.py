# import libraries
import os

# import modules
import ao3interactions as ao3int
import htmlparsing as htp
import datamanipulation as dm

# pyqt gui imports
# used this tutorial as the basis of my pyqt development: https://www.pythonguis.com/pyqt6-tutorial/
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit,
    QDial, QDoubleSpinBox, QFontComboBox, QLabel, QLCDNumber, QLineEdit,
    QMainWindow, QProgressBar, QPushButton, QRadioButton, QSlider,
    QSpinBox, QTimeEdit, QVBoxLayout, QWidget, QTabWidget, QDialog, 
    QDialogButtonBox)

class CustomDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        (title, msg) = parent.get_dlg()

        self.setWindowTitle(title)
        self.setMinimumSize(QSize(400, 200))

        layout = QVBoxLayout()
        
        layout.addWidget(QLabel(msg))

        QBtn = QDialogButtonBox.StandardButton.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        layout.addWidget(self.buttonBox)
        
        self.setLayout(layout)

# setting the main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # super variables
        self.dlg_type : str = "General"
        self.dlg_status : str = "Dialog Triggered in General"

        self.username : str = None
        self.password : str = None
        self.filepath = './gui_test/'
        self.source : str = None
        self.archive : dm.pd.DataFrame = None

        self.col_current = None
        self.search_item = None
        self.r_low = -1
        self.r_high = -1

        # start defining window
        self.setWindowTitle("Cor's AO3 Helper")
        # self.setFixedSize(QSize(800, 600))
        self.setMinimumSize(QSize(800, 600))

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        # header tab
        l1 = QVBoxLayout()
        
        self.intro = QLabel("Meowdy! Welcome to Cor's AO3 Helper.")
        self.intro.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        l1.addWidget(self.intro)
        
        # adding instructions might be useful

        self.sayHello = QLabel()
        self.sayHello.setPixmap(QPixmap("cheer.png"))
        self.sayHello.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        l1.addWidget(self.sayHello)

        self.tab1 = QWidget()
        self.tab1.setLayout(l1)
        self.tabs.addTab(self.tab1, "Intro")

        # - login/load tab
        l2 = QVBoxLayout()

        self.user = QLineEdit()
        self.user.setPlaceholderText("What's your AO3 Username?")
        l2.addWidget(self.user)

        self.passw = QLineEdit()
        self.passw.setPlaceholderText("What's your AO3 Password? Promise I'm not stealing :x")
        l2.addWidget(self.passw)

        self.login = QPushButton("Get Your AO3 Marked for Later List!")
        self.login.clicked.connect(self.attempt_login)
        l2.addWidget(self.login)

        self.tab2 = QWidget()
        self.tab2.setLayout(l2)
        self.tabs.addTab(self.tab2, "Load")

        # - filter item tab

        # - filter range tab

        # - sort tab

        # - extra tab

        # - main window displaying stats (x of y) and list?

        # playing around with fields i might need

        # single line text input
        # getting search item
        #self.search = QLineEdit()
        #self.search.setMaxLength(30)
        #self.search.setPlaceholderText("What do you want to search?")
        #self.search.textEdited.connect(self.text_edited)

        # numeric input
        #self.low = QSpinBox()
        #self.low.setMinimum(0)
        #self.low.valueChanged.connect(self.lowvalue_changed) 

        #self.high = QSpinBox()
        #self.high.setMinimum(0)
        #self.high.valueChanged.connect(self.highvalue_changed) 

        # combo box for selecting column with formal name input
        #self.columns = QComboBox()
        #self.columns.addItems(["work_id", "link", "title", "author", "rating", "warnings", 
        #                  "fandoms", "ships", "characters", "freeforms", "word_count", 
        #                  "chapter_count", "series", "kudos", "hits", "last_update", 
        #                  "last_visit", "visit_num", "last_known_page", "html"])
        #self.columns.currentTextChanged.connect(self.text_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def get_dlg(self):
        return (self.dlg_type, self.dlg_status)
    
    def reset_dlg(self):
        self.dlg_type = "General"
        self.dlg_status = "Dialog Triggered in General"

    def attempt_login(self):
        self.dlg_type = "Loading Marked for Later"

        self.username = self.user.text()
        self.user.clear()
        self.password = self.passw.text()
        self.passw.clear()

        #mfl_pgs_gui = ao3int.getMFL_gui(username, password)
        #mfl_pgs = mfl_pgs_gui[1]
        
        # for testing dialog box
        mfl_pgs_gui = [0]
        
        match mfl_pgs_gui[0]:
            case 0:
                self.dlg_status = "Sorry, a page error occurred."
            case 1:
                self.dlg_status = "Either you have no works Marked for Later or log in failed. Please check and try again."
            case 2:
                self.dlg_status = "Found your works okay! There are " #+ mfl_pgs.size() + "."
            case _:
                self.dlg_status = "How did you get here...Something went terribly wrong..."
        
        dlg = CustomDialog(self)
        dlg.exec()
        self.reset_dlg()


# one QApplication instance per application
# app = QApplication(sys.argv) # if you want to pass in args
app = QApplication([])

window = MainWindow()
window.show()  # windows hidden by default

# start event loop.
app.exec()
