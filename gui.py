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
        self.fandom_frame : dm.pd.DataFrame = None
        self.ship_frame : dm.pd.DataFrame = None
        self.other_frame : dm.pd.DataFrame = None
        self.columns : list = ['work_id', 'title', 'author', "fandoms", "ships"]
        self.frame_col : str = "freeforms"
        self.frame_height = 20
        self.table = None

        self.col_current = None

        # start defining window
        self.setWindowTitle("Cor's AO3 Helper")
        # self.setFixedSize(QSize(800, 600))
        self.setMinimumSize(QSize(800, 1000))

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        # -- header tab
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

        # -- login/load tab
        l2 = QVBoxLayout()

        self.load_blurb = QLabel("To load from AO3, all three fields are necessary. To load from file, only last is required.\n" +
                                "To reset after filtering/sorting, press [load from file] with the file name still entered.")
        self.load_blurb.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        l2.addWidget(self.load_blurb)

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
        l2.addWidget(self.fileload)

        self.tab2 = QWidget()
        self.tab2.setLayout(l2)
        self.tabs.addTab(self.tab2, "Load")

        # -- save/export
        l3 = QVBoxLayout()

        self.outfile = QLineEdit()
        self.outfile.setPlaceholderText("What would you like to name the export?")
        l3.addWidget(self.outfile)

        self.filesave = QPushButton("Save Current Archive")
        self.filesave.clicked.connect(self.attempt_filesave)
        l3.addWidget(self.filesave)

        self.export = QPushButton("Export to HTML")
        self.export.clicked.connect(self.html_export)
        l3.addWidget(self.export)

        self.tab3 = QWidget()
        self.tab3.setLayout(l3)
        self.tabs.addTab(self.tab3, "Export")
        
        # -- filter item tab
        # all cols: ["work_id", "link", "title", "author", "rating", "warnings", 
        #            "fandoms", "ships", "characters", "freeforms", "word_count", 
        #            "chapter_count", "series", "kudos", "hits", "last_update", 
        #            "last_visit", "visit_num", "last_known_page", "html"]
        l4 = QVBoxLayout()

        self.fi_cols = QComboBox()
        self.fi_cols.addItems(["work_id", "title", "author", "rating", "warnings", 
                            "fandoms", "ships", "characters", "freeforms", "series"])
        l4.addWidget(self.fi_cols)

        self.filter_item = QLineEdit()
        self.filter_item.setPlaceholderText("What item would you like to search?")
        l4.addWidget(self.filter_item)

        self.exclude = QCheckBox("Exclude")
        l4.addWidget(self.exclude)

        self.ifilter = QPushButton("Filter on Item")
        self.ifilter.clicked.connect(self.item_filter)
        l4.addWidget(self.ifilter)

        self.tab4 = QWidget()
        self.tab4.setLayout(l4)
        self.tabs.addTab(self.tab4, "Filter Item")

        # -- filter range tab
        l5 = QVBoxLayout()

        self.range_desc = QLabel("Enter your lower number in the top box and higher in the bottom box, inclusive.")
        l5.addWidget(self.range_desc)

        self.fr_cols = QComboBox()
        self.fr_cols.addItems(["word_count", "kudos", "hits", "visit_num", "last_known_page"])
        l5.addWidget(self.fr_cols)

        self.low = QSpinBox()
        self.low.setMaximum(999999999)
        self.low.setSuffix("  min")
        #self.low.valueChanged.connect(self.lowvalue_changed) 
        l5.addWidget(self.low)

        self.high = QSpinBox()
        self.high.setMaximum(999999999)
        self.high.setSuffix("  max")
        #self.high.valueChanged.connect(self.highvalue_changed) 
        l5.addWidget(self.high)

        self.rfilter = QPushButton("Filter on Range")
        self.rfilter.clicked.connect(self.range_filter)
        l5.addWidget(self.rfilter)

        self.tab5 = QWidget()
        self.tab5.setLayout(l5)
        self.tabs.addTab(self.tab5, "Filter Range")

        # -- sort tab
        l6 = QVBoxLayout()

        self.sort_cols = QComboBox()
        self.sort_cols.addItems(["work_id", "title", "author", "rating", "fandoms", 
                               "word_count", "chapter_count", "kudos", "hits", 
                               "last_update", "last_visit", "visit_num", "last_known_page"])
        l6.addWidget(self.sort_cols)

        self.ascend = QCheckBox("Ascending")
        l6.addWidget(self.ascend)

        self.to_sort = QPushButton("Sort")
        self.to_sort.clicked.connect(self.sort)
        l6.addWidget(self.to_sort)

        self.tab6 = QWidget()
        self.tab6.setLayout(l6)
        self.tabs.addTab(self.tab6, "Sort")

        # -- hall of fame tab
        self.l7 = QHBoxLayout()

        self.tab7 = QWidget()
        self.tab7.setLayout(self.l7)
        self.tabs.addTab(self.tab7, "Hall of Frame") #this joke is for me

        # end tabs
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)

        # display list in main window below tabs
        self.display = QLabel("Works will display here!")
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
        self.columns = ['work_id', 'title', 'author', "fandoms", "ships"]
        self.table_display()

    def attempt_filesave(self):
        dm.storeArchive(self.archive, self.filepath + self.outfile.text() + ".csv")
        self.dlg_type = "Saved Archive"
        self.dlg_status = "Archive should be saved; please double-check at target location."
        dlg = CustomDialog(self)
        dlg.exec()
        self.reset_dlg()

    def html_export(self):
        with open(self.filepath + self.outfile.text() + '.html', 'w', encoding='utf-8') as f:
            f.write(dm.getAllHTML(self.archive))
        self.dlg_type = "Saved HTML"
        self.dlg_status = "HTML should have exported; please double-check at target location."
        dlg = CustomDialog(self)
        dlg.exec()
        self.reset_dlg()

    def item_filter(self):
        self.col_current = self.fi_cols.currentText()
        self.archive = dm.filterItem(self.archive, self.col_current, self.filter_item.text(), not self.exclude.isChecked())
        self.table_display()

    def range_filter(self):
        if self.low.value() > self.high.value():
            self.dlg_type = "Filter Range Issue"
            self.dlg_status = "Minimum was set lower than maximum."
            dlg = CustomDialog(self)
            dlg.exec()
            self.reset_dlg()
        else:
            self.col_current = self.fr_cols.currentText()
            self.archive = dm.filterRange(self.archive, self.col_current, self.low.value(), self.high.value())
            self.table_display()

    def sort(self):
        self.col_current = self.sort_cols.currentText()
        self.archive = dm.sortBy(self.archive, self.col_current, self.ascend.isChecked())
        self.table_display()
        
    def table_display(self):
        if self.col_current is not None and self.col_current not in self.columns:
            self.columns.append(self.col_current)

        if self.archive is None:
            self.dlg_type = "Display Table Error"
            self.dlg_status = "No Archive to Display"
            dlg = CustomDialog(self)
            dlg.exec()
            self.reset_dlg()
            return
        
        self.display.setText("Showing " + str(dm.countRows(self.archive)) + " works.")
        
        if self.table is None:
            self.table = QTableView()
            self.model = TableModel(self.archive.loc[:, self.columns])
            self.table.setModel(self.model)
            self.layout.addWidget(self.table)
        else:
            self.model.layoutAboutToBeChanged.emit()
            self.model.set_dataframe(self.archive.loc[:, self.columns])
            self.model.layoutChanged.emit()
            
        self.update_hof()

    def update_hof(self):
        if self.fandom_frame is None:
            self.fandom_frame = QTableView()
            self.fandom_model = TableModel(dm.topTags(self.archive, "fandoms").head(self.frame_height))
            self.fandom_frame.setModel(self.fandom_model)
            self.l7.addWidget(self.fandom_frame)

            self.ships_frame = QTableView()
            self.ships_model = TableModel(dm.topTags(self.archive, "ships").head(self.frame_height))
            self.ships_frame.setModel(self.ships_model)
            self.l7.addWidget(self.ships_frame)

            self.other_frame = QTableView()
            self.other_model = TableModel(dm.topTags(self.archive, self.frame_col).head(self.frame_height))
            self.other_frame.setModel(self.other_model)
            self.l7.addWidget(self.other_frame)
        
        else:
            self.fandom_model.layoutAboutToBeChanged.emit()
            self.fandom_model.set_dataframe(dm.topTags(self.archive, "fandoms").head(self.frame_height))
            self.fandom_model.layoutChanged.emit()
            
            self.ships_model.layoutAboutToBeChanged.emit()
            self.ships_model.set_dataframe(dm.topTags(self.archive, "ships").head(self.frame_height))
            self.ships_model.layoutChanged.emit()
            
            self.other_model.layoutAboutToBeChanged.emit()
            self.other_model.set_dataframe(dm.topTags(self.archive, self.frame_col).head(self.frame_height))
            self.other_model.layoutChanged.emit()


# one QApplication instance per application
# app = QApplication(sys.argv) # if you want to pass in args
app = QApplication([])

window = MainWindow()
window.show()  # windows hidden by default

# start event loop.
app.exec()
