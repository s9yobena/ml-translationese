import lang.en.translationese as translationese
from lang.en.translationese.__init__ import Analysis
import glob
import core
import re

# The results model dictionary is used to distinguish between attributes for 
# which the analysis of one text returns one value (e.g., lexical_density) and
# those where the analysis of one text returns many values (e.g., 
# function_words).
resultsModel = {"lexical_density": "1x1", "function_words":"1xN"}


class TaggedFile(Analysis):
    def __init__(self, __tagFile, __tokens, __sentences=None):
        self._tagFile = __tagFile
        self._tokens = __tokens
        self._sentences = __sentences

    def pos_tags(self):
        return self._tagFile

    def tokens(self):
        return self._tokens

    def sentences(self):
        return self._sentences

class AnalysisResult:
    def __init__(self, _model="", _key="", _value=""):
        self.model = _model
        self.key = _key
        self.value = _value

class TextAnalyser:
    """Computes the attributes related to a specific text in a file"""

    def __init__(self):
        self.fileName=""
        self.posTagSet = ""
        self.analyzerModule = 0
        self.tmpAnalysisResult = 0
        self.analysisResult = {}
        self._lang = ""
        self._format = ""
    
    def setFile(self, _fileName):
        self.fileName = _fileName

    def setLanguage(self, __lang):
        core.posTagSetLang = __lang
        self._lang = __lang

    def setFormat(self, __format):
        self._format = __format
        
    def __setAnalyserModule(self, _analyserModule):
        self.analyzerModule = __import__('lang.{lang}.translationese.{modul}'
                                         .format(lang = self._lang, 
                                                 modul = _analyserModule),
                                         globals=globals(), 
                                         fromlist='translationese')

    def __analyzeFile(self, tagFile=None, variant=None, _printPosTags=False):
        self.tmpAnalysisResult = 0
        if tagFile:
            if _printPosTags:                
                print "printing pos tags", tagFile.pos_tags()
                print "printing tokens", tagFile.tokens(),"\n"
                print "printing sentencess", tagFile.sentences()

            if variant is not None:
                self.tmpAnalysisResult = self.analyzerModule.quantify_variant(
                    tagFile, variant)
            else:
                self.tmpAnalysisResult = self.analyzerModule.quantify(tagFile)
        else:
            with translationese.Analysis(filename=self.fileName) as analysis:
                if _printPosTags:
                    print "printing pos tags", analysis.pos_tags()
                    print "printing tokens", analysis.tokens(),"\n"
                    print "printing sentences", analysis.sentences()
                if variant is not None:
                    self.tmpAnalysisResult = self.analyzerModule.quantify_variant(
                        analysis, variant)
                else:
                    self.tmpAnalysisResult = self.analyzerModule.quantify(analysis)

    def computeAttribute(self,_attribute, _printAnalysisResults = False):
        self.__setAnalyserModule(_attribute)
        if self._format=="txt":
            self.__analyzeFile()
        elif self._format=="freeling":
            matches = []
            with open(self.fileName,"r") as csvfile:
                matches = [re.findall("([\w]+|\.)[\s]+([\w]+)",line) for line in csvfile]
                t_pos_tags = [item for sublist in matches for item in sublist]
                t_tokens = [i[0] for i in t_pos_tags]
                t_sentences = []
                t_sentence = ""
                for t in t_tokens:
                    if t==".":
                        t_sentence = t_sentence[0:-1]+"."
                        t_sentences.append(t_sentence)
                        t_sentence=""
                    else:
                        t_sentence = t_sentence+t+" "
                
            tf = TaggedFile(t_pos_tags, t_tokens, t_sentences)
            self.__analyzeFile(tf)
                 
        if _printAnalysisResults:
            print self.tmpAnalysisResult

        if resultsModel[_attribute] == "1x1":
            self.analysisResult[_attribute] = \
                AnalysisResult(resultsModel[_attribute],
                               _attribute, 
                               # get only one value; internally, 
                               # tmpAnalysisResult is a dict. with only one item.
                               self.tmpAnalysisResult[_attribute]) 
        elif resultsModel[_attribute] == "1xN":
            self.analysisResult[_attribute] = \
                AnalysisResult(resultsModel[_attribute],
                               _attribute, 
                               # get all the values; internally,
                               # tmpAnalysisResult is a dict with N items.
                               self.tmpAnalysisResult)

        
    def getResult(self, _attribute):
        return self.analysisResult[_attribute].value

    def getModel(self, _attribute):
        return self.analysisResult[_attribute].model


class DirAnalyser:
    def __init__(self, _dir, _lang, _format):
        self.__dir = _dir
        self.__lang = _lang
        self.__format = _format

    def analyse(self, _attributes):
        analyserList = []
        # search for .txt files in __dir 
        for textF in glob.glob(self.__dir+"/"+self.__lang+
                               "/*."+self.__format):
            analyser = TextAnalyser()
            analyser.setFile(textF)
            analyser.setLanguage(self.__lang)
            analyser.setFormat(self.__format)
            for att in _attributes:
                analyser.computeAttribute(att)
            analyserList.append(analyser)
        return analyserList

