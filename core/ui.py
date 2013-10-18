from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self, data):
        QMainWindow.__init__(self)

        self.__dataModel = data

        self.mainWidget = QWidget(self) # dummy to contain the layout manager
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle('ML Translationese')
        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)

        self.resultsView = QTableView()
        self.resultsView.setModel(self.__dataModel)
        
        self.mainLayout.addWidget(self.resultsView)
        
        self.quitButton = QPushButton('Close', self)
        self.connect(self.quitButton, SIGNAL('clicked()'), SLOT('close()'))

        self.mainLayout.addWidget(self.quitButton)

        
    def close(self):
        self.close

class AnalysisData(QAbstractTableModel):
    def __init__(self, analysisData = [], headers = [], parent = None):
        QAbstractTableModel.__init__(self, parent)
        self.__analysisData = analysisData
        self.__headers = headers

    def rowCount(self, parent):
        return len(self.__analysisData)

    def columnCount(self, parent):
        return len(self.__headers)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
    def data(self, index, role ):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__analysisData[row].getResult(self.__headers[column])

            return value

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                    return QString(self.__headers[section])
            else:
                    return self.__analysisData[section].fileName
    

