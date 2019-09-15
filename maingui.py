import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QTabWidget, QPushButton, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
import startup
import excel_import

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        self.master_state = startup.startup(CONFIG='/Users/iaricanli/IRSGRAY/main.conf', SERVICE='IRSGRAY')
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()


    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        return files
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.child_tab = QWidget()
        self.irs_tab = QWidget()
        self.report_tab = QWidget()
        self.tabs.resize(500,200)
        
        # Add tabs
        self.tabs.addTab(self.child_tab,"Children")
        self.tabs.addTab(self.irs_tab,"IRS")
        self.tabs.addTab(self.report_tab,"Reports")
        
        # Create first tab
        self.irs_tab.layout = QVBoxLayout(self)
        self.irs_tab.layout.setAlignment(Qt.AlignTop)
        
        btnLoadFile = QPushButton('On press begins the file loading', self)
        btnLoadFile.setToolTip('Load in an IRS File')
        btnLoadFile.clicked.connect(LoadFile_Onclick)
        
        self.btnLoadFile = btnLoadFile
        self.irs_tab.layout.addWidget(self.btnLoadFile)
        self.irs_tab.setLayout(self.irs_tab.layout)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


@pyqtSlot()
def LoadFile_Onclick(self):
    files = self.openFileNamesDialog()
    for file in files:
        excel_import.Import_IRS_01(self.master_state, file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())