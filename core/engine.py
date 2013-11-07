import  lang.en.translationese as translationese
import glob
import core

class TaggedFile:
    def __init__(self, __tagFile, __tokens):
        self._tagFile = __tagFile
        self._tokens = __tokens

    def pos_tags(self):
        return self._tagFile

    def tokens(self):
        return self._tokens



class TextAnalyser:
    """Computes the attributes related to a specific text in a file"""

    def __init__(self):
        self.fileName=""
        self.posTagSet = ""
        self.analyzerModule = 0
        self.tmpAnalysisResult = 0
        self.analysisResult = {}
        self._lang = ""
    
    def setFile(self, _fileName):
        self.fileName = _fileName

    def setLanguage(self, __lang):
        core.posTagSetLang = __lang
        self._lang = __lang
        
    def __setAnalyserModule(self, _analyserModule):
        self.analyzerModule = __import__('lang.{lang}.translationese.{modul}'
                                         .format(lang = self._lang, 
                                                 modul = _analyserModule),
                                         globals=globals(), 
                                         fromlist='translationese')

    def __analyzeFile(self, tagFile=None, variant=None, _printPosTags=False):
        self.tmpAnalysisResult = 0
        if tagFile:
            if variant is not None:
                self.tmpAnalysisResult = self.analyzerModule.quantify_variant(
                    tagFile, variant)
            else:
                self.tmpAanalysisResult = self.analyzerModule.quantify(tagFile)
        else:
            with translationese.Analysis(filename=self.fileName) as analysis:
                if _printPosTags:
                    print "printing pos tags", analysis.pos_tags()
                    print "printing tokens", analysis.tokens(),"\n"
                if variant is not None:
                    self.tmpAnalysisResult = self.analyzerModule.quantify_variant(
                        analysis, variant)
                else:
                    self.tmpAanalysisResult = self.analyzerModule.quantify(analysis)

    def computeAttribute(self,_attribute, _printAnalysisResults = False):
        self.__setAnalyserModule(_attribute)
        self.__analyzeFile()

        if _printAnalysisResults:
            print self.tmpAanalysisResult
        self.analysisResult[_attribute] = self.tmpAanalysisResult[_attribute]
        
        
    def getResult(self, _attribute):
        return self.analysisResult[_attribute]

class DirAnalyser:
    def __init__(self, _dir, _lang):
        self.__dir = _dir
        self.__lang = _lang

    def analyse(self, _attributes):
        analyserList = []
        # search for .txt files in __dir 
        for textF in glob.glob(self.__dir+"/"+self.__lang+"/*.txt"):
            analyser = TextAnalyser()
            analyser.setFile(textF)
            analyser.setLanguage(self.__lang)
            for att in _attributes:
                analyser.computeAttribute(att)
            analyserList.append(analyser)
        return analyserList

