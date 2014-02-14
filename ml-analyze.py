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
                      dest="format", default="txt")

    parser.add_option("-m","--module", action="store", type="string",
                      dest="module", default=None, 
                      help="Lexical feature to compute; default: lexical_density")


    parser.add_option("--nw","--no-window", action="store_true",
                      dest="nw", default=False, help="Don't use the GUI")

    parser.add_option("-i","--input", action="store", type="string",
                      dest="input_file", default=None)

    
    (options, args) = parser.parse_args()
    
    # check arguments
    if options.module is None:
        print "Please provide a module name"
        parser.print_help()
        return

    attributes = []
    attributes.append(options.module)

    analyserList = []
    dirAnalyser = DirAnalyser(options.textDir, options.lang, options.format,
                              options.input_file)
    analyserList = dirAnalyser.analyse(attributes)

    if options.nw:

        if analyserList[0].getModel(attributes[0]) == "1x1":
            print repr("File Name"), repr(attributes[0])
            for a in analyserList:
                print repr(a.fileName), \
                    repr("{0:.3f}".format(a.getResult(attributes[0])))

        elif analyserList[0].getModel(attributes[0]) == "1xN":
            for a in analyserList:
                print
                print "File Name: ", a.fileName
                print attributes[0],": "
                for k,v in a.getResult(attributes[0]).iteritems():
                    if v != float(0):
                        print k,v
                # print repr(a.fileName), \
                #     repr("{0:.3f}".format(a.getResult(attributes[0])))
                

    else:
        app = QApplication(sys.argv)
        app.setApplicationName('multiple language translationese')
    
        dataModel = AnalysisData(analyserList, attributes) 
        mainWindow = MainWindow(dataModel)
        mainWindow.update()
        mainWindow.show()

        sys.exit(app.exec_())


if __name__=='__main__':
    main()
