"""\
The frequency of tokens that are `not` nouns, adjectives, adverbs or verbs.
"""

__author__ = "Gal Star"
__email__ = "gal.star3051@gmail.com"

from core import mlPOS, posTagSetLang
import core

def quantify(analysis):
    """Quantify lexical density."""
    all_tags = analysis.tokens()
    
    def is_lexical_density(letter):    
        # the commented code is kept for later reference.
        # is_not_verb = letter[0] !='V'
        # is_not_noun = letter[0] !='N'
        # is_not_adjective = letter[0] !='J'
        # is_not_adverb = letter[0] !='R'
        is_not_verb = letter[0] !=core.mlPOS[(core.posTagSetLang,"verb","vrb")]
        is_not_noun = letter[0] !=core.mlPOS[(core.posTagSetLang,"noun","n")]
        is_not_adjective = letter[0] !=core.mlPOS[(core.posTagSetLang,"adjective","adj")]
        is_not_adverb = letter[0] !=core.mlPOS[(core.posTagSetLang,"adverb","adv")]
        
        
        return is_not_verb and is_not_noun and is_not_adverb and \
               is_not_adjective
    
    def count_all_lexical_pos_tags():
        text = analysis.pos_tags()
        return len([t for t in text if is_lexical_density(t[1])])
    
    result = float(count_all_lexical_pos_tags()) / len(all_tags)
    return { "lexical_density": result }
