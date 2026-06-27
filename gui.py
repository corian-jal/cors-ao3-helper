# import libraries
import os

# import modules
import ao3interactions as ao3int
import htmlparsing as htp
import datamanipulation as dm

# pyqt gui imports
# used this tutorial as the basis of my pyqt development: https://www.pythonguis.com/pyqt6-tutorial/
from PyQt6.QtCore import QSize, Qt, QAbstractTableModel
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit,
    QDial, QDoubleSpinBox, QFontComboBox, QLabel, QLCDNumber, QLineEdit,
    QMainWindow, QProgressBar, QPushButton, QRadioButton, QSlider,
    QSpinBox, QTimeEdit, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, 
    QDialog, QDialogButtonBox, QTableView)

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

# derived from this guide (pyqt5): https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/
class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

    # seems like a hard reset but i'll take the potential inefficiency
    # esp since # of row/cols can change      
    def set_dataframe(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()

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
        self.table = None
        self.columns : list = ['work_id', 'title', 'author']

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
        # hide text somehow?
        l2.addWidget(self.passw)

        self.file = QLineEdit()
        self.file.setPlaceholderText("What would you like to name this saved file? / File to load?")
        l2.addWidget(self.file)

        self.login = QPushButton("Get Your AO3 Marked for Later List!")
        self.login.clicked.connect(self.attempt_login)
        l2.addWidget(self.login)

        self.fileload = QPushButton("Load From Saved File Instead")
        self.fileload.clicked.connect(self.attempt_fileload)
        l2.addWidget(self.fileload) # add feedback to know if worked

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

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)

        # display list in main window below tabs
        self.display = QLabel("Works should display below here!")
        self.layout.addWidget(self.display)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def get_dlg(self):
        return (self.dlg_type, self.dlg_status)
    
    def reset_dlg(self):
        self.dlg_type = "General"
        self.dlg_status = "Dialog Triggered in General"

    def attempt_login(self):
        self.dlg_type = "Loading Marked for Later"
        self.dlg_status = "App will be unresponsive while pulling. Do not close.\nSee CLI for status info."
        dlg = CustomDialog(self)
        dlg.exec()

        os.system('cls')
        self.username = self.user.text()
        self.password = self.passw.text()
        self.user.clear()
        self.passw.clear()
        mfl_pgs_gui = ao3int.getMFL_gui(self.username, self.password)

        mfl_pgs = mfl_pgs_gui[1]
        
        match mfl_pgs_gui[0]:
            case 0:
                self.dlg_status = "Sorry, a page error occurred."
            case 1:
                self.dlg_status = "Either you have no works Marked for Later or log in failed. Please check and try again."
            case 2:
                self.dlg_status = "Found your works okay! There are " + str(len(mfl_pgs)) + " pages."
            case _:
                self.dlg_status = "How did you get here...Something went terribly wrong..."
        
        dlg = CustomDialog(self)
        dlg.exec()

        library = []
        num = 1
        for mfl_pg in mfl_pgs:
            print("Parsing page " + str(num) + "...")
            library = library + htp.mflPageToFicList(mfl_pg, num)
            num += 1
        self.dlg_status = str(len(library)) + " works found."
        dlg = CustomDialog(self)
        dlg.exec()
            
        self.archive = dm.createArchive(library)

        self.source = self.filepath + self.file.text() + '.csv'
        dm.storeArchive(self.archive, self.source)
        self.archive = dm.loadArchive(self.source)

        self.dlg_status = "Exported to '" + self.source + "'."
        dlg = CustomDialog(self)
        dlg.exec()

        self.reset_dlg()

        self.table_display()

    def attempt_fileload(self):
        self.source = self.filepath + self.file.text() + '.csv'
        self.archive = dm.loadArchive(self.source)
        self.table_display()
        
    def table_display(self):
        if self.archive is None:
            self.dlg_type = "Display Table Error"
            self.dlg_status = "No Archive to Display"
            dlg = CustomDialog(self)
            dlg.exec()
            self.reset_dlg()
        
        elif self.table is None:
            self.table = QTableView()
            self.model = TableModel(self.archive.loc[:, self.columns])
            self.table.setModel(self.model)
            self.layout.addWidget(self.table)

        else:
            self.model.layoutAboutToBeChanged.emit()
            self.model.set_dataframe(self.archive.loc[:, self.columns])
            self.model.layoutChanged.emit()


# one QApplication instance per application
# app = QApplication(sys.argv) # if you want to pass in args
app = QApplication([])

window = MainWindow()
window.show()  # windows hidden by default

# start event loop.
app.exec()
