#!/usr/bin/python

import glob
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from core.ui import MainWindow, AnalysisData
from core.engine import TextAnalyser, DirAnalyser
from optparse import OptionParser


def main():

    parser = OptionParser();

    parser.add_option("-d","--text-dir", action="store", type="string", 
                      dest="textDir", default="text-dir")
    
    parser.add_option("-l","--lang", action="store", type="string",
                      dest="lang", default="en")

    parser.add_option("-f","--format", action="store", type="string",
                      dest="format", default="text")
    

    (options, args) = parser.parse_args()

    attributes = ["lexical_density"]

    analyserList = []
    dirAnalyser = DirAnalyser(options.textDir, options.lang)
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
