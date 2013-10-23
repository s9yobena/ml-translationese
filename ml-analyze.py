#!/usr/bin/python

import glob
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from core.ui import MainWindow, AnalysisData
from core.engine import TextAnalyser, DirAnalyser


def main():

    # attributes = ["lexical_density","average_pmi","threshold_pmi"]
    attributes = ["lexical_density",]

    analyserList = []
    dirAnalyser = DirAnalyser("text-dir","EN")
    analyserList = dirAnalyser.analyse(attributes)

    app = QApplication(sys.argv)
    app.setApplicationName('multiple language translationese')
    
    dataModel = AnalysisData(analyserList, attributes) 
    mainWindow = MainWindow(dataModel)
    mainWindow.update()
    mainWindow.show()

    sys.exit(app.exec_())


if __name__=='__main__':
    main()
