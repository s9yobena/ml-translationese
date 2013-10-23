import  translationese
import glob
import core


class TextAnalyser:
    """Computes the attributes related to a specific text in a file"""

    def __init__(self):
        self.fileName=""
        self.posTagSet = ""
        self.analyzerModule = 0
        self.tmpAnalysisResult = 0
        self.analysisResult = {}
    
    def setFile(self, _fileName):
        self.fileName = _fileName

    def setLanguage(self, _lang):
        core.posTagSetLang = _lang
        
    def __setAnalyserModule(self, _analyserModule):
        self.analyzerModule = __import__('translationese.%s' % _analyserModule,globals=globals(),
                                         fromlist='translationese')


    def __analyzeFile(self, variant=None, _printPosTags=False):
        self.tmpAnalysisResult = 0
        with translationese.Analysis(filename=self.fileName) as analysis:
            if _printPosTags:
                print "printing analysi", analysis.pos_tags_by_sentence()
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
        for textF in glob.glob(self.__dir+"/*.txt"):
            analyser = TextAnalyser()
            analyser.setFile(textF)
            analyser.setLanguage(self.__lang)
            for att in _attributes:
                analyser.computeAttribute(att)
            analyserList.append(analyser)
        return analyserList

