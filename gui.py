# import sys # to access command line args
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit,
    QDial, QDoubleSpinBox, QFontComboBox, QLabel, QLCDNumber, QLineEdit,
    QMainWindow, QProgressBar, QPushButton, QRadioButton, QSlider,
    QSpinBox, QTimeEdit, QVBoxLayout, QWidget, QTabWidget,
)

# super variables
username = "none"
password = "none"
col_current = "none"
search_item = "none"
r_low = -1
r_high = -1

# setting the main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cor's GUI Experiment")
        # self.setFixedSize(QSize(800, 600))
        self.setMinimumSize(QSize(800, 600))

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)

        # header tab
        l1 = QVBoxLayout()
        
        intro = QLabel("Meowdy! Welcome to Cor's AO3 Helper.")
        intro.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        l1.addWidget(intro)
        
        # adding instructions might be useful

        sayHello = QLabel()
        sayHello.setPixmap(QPixmap("cheer.png"))
        sayHello.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        l1.addWidget(sayHello)

        tab1 = QWidget()
        tab1.setLayout(l1)
        tabs.addTab(tab1, "Intro")

        # - login/load tab
        l2 = QVBoxLayout()

        user = QLineEdit()
        user.setMaxLength(30)
        user.setPlaceholderText("username")
        user.textEdited.connect(self.user_edited)
        l2.addWidget(user)

        passw = QLineEdit()
        passw.setMaxLength(30)
        passw.setPlaceholderText("password")
        passw.textEdited.connect(self.passw_edited)
        l2.addWidget(passw)

        login = QPushButton("Log In to AO3")
        login.clicked.connect(self.attempt_login)
        l2.addWidget(login)

        tab2 = QWidget()
        tab2.setLayout(l2)
        tabs.addTab(tab2, "Load")

        # - filter item tab

        # - filter range tab

        # - sort tab

        # - extra tab

        # - main window displaying stats (x of y) and list?

        # playing around with fields i might need

        # single line text input
        # getting search item
        search = QLineEdit()
        search.setMaxLength(30)
        search.setPlaceholderText("What do you want to search?")
        search.textEdited.connect(self.text_edited)

        # numeric input
        low = QSpinBox()
        low.setMinimum(0)
        low.valueChanged.connect(self.lowvalue_changed) 

        high = QSpinBox()
        high.setMinimum(0)
        high.valueChanged.connect(self.highvalue_changed) 

        # combo box for selecting column with formal name input
        columns = QComboBox()
        columns.addItems(["work_id", "link", "title", "author", "rating", "warnings", 
                          "fandoms", "ships", "characters", "freeforms", "word_count", 
                          "chapter_count", "series", "kudos", "hits", "last_update", 
                          "last_visit", "visit_num", "last_known_page", "html"])
        columns.currentTextChanged.connect(self.text_changed)

        layout = QVBoxLayout()
        widgets = [
            tabs,
            #intro,
            #sayHello,
            #search,
            #low,
            #high,
            #columns,
            #QCheckBox,
            #QComboBox,
            #QDateEdit,
            #QLabel, # static text label
            #QLineEdit,
            #QProgressBar,
            #QPushButton,
            #QRadioButton,
        ]

        for w in widgets:
            layout.addWidget(w)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def user_edited(self, s):
        username = s

    def passw_edited(self, s):
        password = s

    def attempt_login(self):
        # attempt login
        print("To be implemented.")

    def text_edited(self, s):
        search_item = s

    def lowvalue_changed(self, i):
        r_low = i

    def highvalue_changed(self, i):
        r_high = i
    
    def text_changed(self, s): # s is a str
        col_current = s
        # print(s)


# one QApplication instance per application
# app = QApplication(sys.argv) # if you want to pass in args
app = QApplication([])

window = MainWindow()
window.show()  # windows hidden by default

# start event loop.
app.exec()
