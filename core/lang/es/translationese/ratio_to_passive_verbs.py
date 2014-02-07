"""\
We assume that English original texts tend to use the passive form more
excessively than translated texts, due to the fact that the passive voice is
more frequent in English than in some other languages. If an active voice is
used in the source language, translators may prefer not to convert it to the
passive. Passives are defined as the verb be fol- lowed by the POS tag VBN
(past participle). We calculate the ratio of passive verbs to all verbs, and
magnified it by an order of 6.
"""
from core import mlPOS, posTagSetLang
import core

def quantify(analysis):
    """Quantify ratio of passive forms to all verbs."""
    def is_verb(pos_tag):
        # return pos_tag[0] == 'V' and pos_tag[1] == 'B'
        return pos_tag[0] == core.mlPOS[(core.posTagSetLang,"verb","vrb")]
    
    def is_VBN_verb(pos_tag):
        # return pos_tag == 'VBN'
        return pos_tag[0] == core.mlPOS[(core.posTagSetLang,"verb","vrb")] and \
            pos_tag[2] == 'P'
    
    def count_all_verbs():
        result =  float(len([x for (x,y,z) in analysis.pos_tags() if is_verb(y)]))
        return result
   
    def count_all_passive_verbs():
        passive_verbs = 0
        text = analysis.pos_tags()
        for i in range(len(text)):
            if (text[i][1][:2] == 'VS') and (is_VBN_verb(text[i+1][1])):
                passive_verbs += 1
        
        return float(passive_verbs)
    
    result = float(count_all_passive_verbs() / count_all_verbs())
    return { "ratio_to_passive_verbs" : result }
