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

        # my header
        intro = QLabel("Meowdy! Welcome to Cor's AO3 Helper.")
        intro.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        sayHello = QLabel()
        sayHello.setPixmap(QPixmap("cheer.png"))
        sayHello.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # playing around with fields i might need

        # tabbed view
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        
        test = QLineEdit()
        test.setPlaceholderText("hi")
        tabs.addTab(test, "Tab 1")
        
        test2 = QLineEdit()
        test2.setPlaceholderText("hi2")
        tabs.addTab(test2, "Tab 2")

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
            intro,
            sayHello,
            search,
            low,
            high,
            columns,
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
