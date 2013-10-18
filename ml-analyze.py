#!/usr/bin/python

import glob
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from core.ui import MainWindow, AnalysisData
from core.engine import TextAnalyser, DirAnalyser


def main():

    analyserList = []
    dirAnalyser = DirAnalyser("text-dir")
    analyserList = dirAnalyser.analyse()

    app = QApplication(sys.argv)
    app.setApplicationName('multiple language translationese')
    
    dataModel = AnalysisData(analyserList, ["lexical_density", "average_pmi"])
    mainWindow = MainWindow(dataModel)
    mainWindow.show()

    sys.exit(app.exec_())


if __name__=='__main__':
    main()
