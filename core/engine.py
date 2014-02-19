# -*- coding: utf-8 -*-

import lang.en.translationese as translationese
from lang.en.translationese.__init__ import Analysis
import glob
import core
import re
import codecs

# The results model dictionary is used to distinguish between attributes for 
# which the analysis of one text returns one value (e.g., lexical_density) and
# those where the analysis of one text returns many values (e.g., 
# function_words).
resultsModel = {"lexical_density": "1x1",
                "mean_sentence_length": "1x1",
                "function_words":"1xN",
                "pronouns":"1xN",
                "explicit_naming":"1x1",
                "ratio_to_passive_verbs":"1x1",
                "syllable_ratio":"1x1",
                "average_pmi":"1x1",
                "repetitions":"1x1",
                "mean_word_rank":"1x1",
                "mean_word_rank":"1x1"}


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

    # Returns the pos of WORD if word is in _tokens, otherwise returns None.
    def word_pos(self, word):
        for t in self._tagFile:
            if t[0] == word:
                return t[1]
        return None

    # Same as word_pos, but compares word against tokens normalized to lower case.
    def l_word_pos(self, word):
        for t in self._tagFile:
            if t[0].lower() == word:
                return t[1]
        return None


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
        self.analyzerVariants = 0
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
        if hasattr(self.analyzerModule, 'quantify_variant'):
            self.analyzerVariants =  self.analyzerModule.VARIANTS 
   
        print self.analyzerVariants
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

    def computeAttribute(self,_attribute,_variant,_printAnalysisResults = False):
        self.__setAnalyserModule(_attribute)
        if self._format=="txt":
            self.__analyzeFile()
        elif self._format=="freeling":
            matches = []
            with codecs.open(self.fileName,
                             encoding='utf-8', mode="r") as csvfile:
                t_pos_tags = []
                t_tokens = []
                t_sentences = []
                t_sentence = ""
                for line in csvfile:
                    if line == "\n" or line =="#":
                        t_sentences.append(t_sentence)
                        t_sentence=""                        
                        continue
                    else:
                        matches = re.findall("(.+?)[\s]+(.+?)[\s]+(.+?)$",line) 
                        t_pos_tag = matches[0]
                        t_token = t_pos_tag[0]
                        t_sentence = t_sentence+t_token+" "
                        
                        t_pos_tags.append(t_pos_tag)
                        t_tokens.append(t_token)

            tf = TaggedFile(t_pos_tags, t_tokens, t_sentences)
            if self.analyzerVariants == 0:
                self.__analyzeFile(tf)
            else:
                # TODO: make sure the use supplied variant is valid
                self.__analyzeFile(tf, _variant)
                 
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
    def __init__(self, _dir, _lang, _format, _input_file):
        self.__dir = _dir
        self.__lang = _lang
        self.__format = _format
        self.__input_file = _input_file

    def analyse(self, _attributes, _variant):
        analyserList = []
        # search for .txt files in __dir 
        if self.__input_file is None:
            for textF in glob.glob(self.__dir+"/"+self.__lang+
                                   "/*."+self.__format):
                analyser = TextAnalyser()
                analyser.setFile(textF)
                analyser.setLanguage(self.__lang)
                analyser.setFormat(self.__format)
                for att in _attributes:
                    analyser.computeAttribute(att, _variant)
                    analyserList.append(analyser)
            return analyserList
        else:
            analyser = TextAnalyser()
            analyser.setFile(self.__input_file)
            analyser.setLanguage(self.__lang)
            analyser.setFormat(self.__format)
            for att in _attributes:
                analyser.computeAttribute(att, _variant)
                analyserList.append(analyser)
            return analyserList

