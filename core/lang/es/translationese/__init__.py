# -*- coding: utf-8 -*-

from .... import memoize
import math
import os
from utils import flatten_list, sparse_dict_increment
# from translationese.utils import flatten_list, sparse_dict_increment

if os.environ.get("READTHEDOCS", None) != 'True':
    import nltk
    from nltk.tag import pos_tag

expected_chunk_size = 2000.0

class Analysis(object):
    """This class represent and caches an :mod:`nltk` analysis of a given text.
    The text can be initialized either from a file (``stream``) or from
    ``fulltext``.

    All analyses performed by this class are cached using :mod:`memoize`, so
    they can be re-run cheaply. Also, when text is loaded using ``filename``,
    this object will be saved using :mod:`pickle` to a file with ``.analysis``
    appended to its name. Consequent analyses will load cached data.
    """

    def __init__(self, fulltext=None, stream=None, filename=None):
        self.filename = None
        if fulltext:
            self.fulltext = fulltext
        elif stream:
            self.fulltext = stream.read()
        elif filename:
            self.filename = filename
            self.fulltext = open(filename, "r").read()
            self.picklefile = "%s.analysis" % filename
        else:
            raise AttributeError()

    def __enter__(self):
        self.loadcache()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if traceback is not None:
            # An exception was thrown, do not save pickle
            return False
        self.savecache()

    def loadcache(self):
        if not self.picklefile:
            raise AttributeError('Cannot use Analysis in "with" block '
                                 'unless constructed with a filename.')
        memoize.load(self, self.picklefile)

    def savecache(self):
        memoize.dump(self, self.picklefile)

    @memoize.memoize
    def sentences(self):
        return nltk.sent_tokenize(self.fulltext)

    @memoize.memoize
    def case_tokens(self):
        """Same as ``tokens``, but case-sensitive."""
        # We tokenize into sentences and then into words due to a warning
        # in the NLTK API doc to only word_tokenize single sentences.
        tokens = []

        for sentence in self.sentences():
            tokens += nltk.word_tokenize(sentence)

        return tokens

    @memoize.memoize
    def pos_tags_by_sentence(self):
        """Return part-of-speech tags, split by sentence.
        Case-sensitive, as part-of-speech tagging is case-sensitive by nature
        (nouns vs. proper nouns).

        >>> Analysis("I am fine. How are you?").pos_tags_by_sentence()
        ... # doctest: +NORMALIZE_WHITESPACE
        [[('I', 'PRP'), ('am', 'VBP'), ('fine', 'NN'), ('.', '.')],
        [('How', 'WRB'), ('are', 'VBP'), ('you', 'PRP'), ('?', '.')]]
        """
        return nltk.batch_pos_tag(self.case_tokenized_sentences())

    @memoize.memoize
    def pos_tags(self):
        """Return part-of-speech tags, for the entire document.

        >>> Analysis("I am fine. How are you?").pos_tags()
        ... # doctest: +NORMALIZE_WHITESPACE
        [('I', 'PRP'), ('am', 'VBP'), ('fine', 'NN'), ('.', '.'),
        ('How', 'WRB'), ('are', 'VBP'), ('you', 'PRP'), ('?', '.')]
        """
        return flatten_list(self.pos_tags_by_sentence())

    @memoize.memoize
    def tokenized_sentences(self):
        """List of sentences, tokenized as lowercase.

        >>> Analysis("Hello. How are you?").tokenized_sentences()
        [['hello', '.'], ['how', 'are', 'you', '?']]
        """
        lowercase_sentences = [ s.lower() for s in self.sentences() ]
        return [ nltk.word_tokenize(s) for s in lowercase_sentences ]

    @memoize.memoize
    def case_tokenized_sentences(self):
        """List of sentences, tokenized, case-sensitive.

        >>> Analysis("Hello. How are you?").case_tokenized_sentences()
        [['Hello', '.'], ['How', 'are', 'you', '?']]
        """
        return [ nltk.word_tokenize(s) for s in self.sentences() ]

    @memoize.memoize
    def tokens(self):
        """Tokens are always in lowercase. For tokens with the original
        case, use ``case_tokens()``."""
        return [ w.lower() for w in self.case_tokens() ]

    @memoize.memoize
    def tokens_set(self):
        """Same as ``tokens``, but as a ``set``."""
        return set(self.tokens())

    @memoize.memoize
    def histogram(self):
        """Return a histogram of tokens in the text.
        
        >>> Analysis("Hello, hello world.").histogram()
        {'world': 1, '.': 1, 'hello': 2, ',': 1}
        """
        result = {}
        for t in self.tokens():
            sparse_dict_increment(result, t)
        return result

    @memoize.memoize
    def histogram_normalized(self):
        """Same as ``histogram``, but normalized by number of tokens."""
        items = self.histogram().items()
        num_tokens = float(len(self.tokens()))
        items_normalized = [ (x, y / num_tokens) for x, y in items ]
        return dict(items_normalized)

    def bigrams(self):
        """Returns a histogram of bigrams in the text.
        
        >>> Analysis("Hello hello hello world").bigrams()
        {('hello', 'world'): 1, ('hello', 'hello'): 2}
        """
        result = {}
        for i in range(len(self.tokens()) - 1):
            bigram = (self.tokens()[i], self.tokens()[i + 1])
            sparse_dict_increment(result, bigram)
        return result

    def pmi(self):
        """Returns a dictionary with the PMI of each bigram. Given a bigram
        ``w1,w2``, its PMI is ``log(freq(w1w2)/(freq(w1)*freq(w2)))``."""
        num_bigrams = float(len(self.tokens()) - 1)
        bigrams_normalized = dict([ (x, y / num_bigrams)
                                    for (x, y) in self.bigrams().items() ])
        freq = self.histogram_normalized()

        bigram_pmi = lambda bigram, bigram_freq: \
                math.log(bigram_freq / (freq[bigram[0]] * freq[bigram[1]]))

        bigram_pmi_pairs = [
                (bigram, bigram_pmi(bigram, bigram_freq))
                for (bigram, bigram_freq) in bigrams_normalized.items()
                ]

        return dict(bigram_pmi_pairs)

import exceptions
class MissingVariant(exceptions.Exception):
    """Exception thrown when no variant was specified when quantifying using
    a module that requires a variant specification."""
    pass

class NoVariants(exceptions.Exception):
    """Exception thrown when a variant was specified when quantifying using
    a module that does not support variant specification."""
    pass

class NoSuchVariant(exceptions.Exception):
    """Exception thrown when an invalid variant was specified when quantifying
    using a module that supports variant specification."""
    def __init__(self):
        Exception.__init__(self, "Invalid variant requested")
