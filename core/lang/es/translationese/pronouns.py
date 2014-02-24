# -*- coding: utf-8 -*-

"""\
This hypothesis checks whether pronouns taken from
`http://nlp.lsi.upc.edu/freeling/doc/tagsets/tagset-es.html#pronombres` alone
can yield a high classification accuracy. Each pronoun in the corpus is a
feature, whose value is the normalized frequency of its occurrences in the
chunk.
"""

PRONOUNS = [
    (u"yo",None),
    (u"me",None),
    (u"mí",None),
    (u"nos",None),
    (u"nosotras",None),
    (u"nosotros",None),
    (u"conmigo",None),
    (u"te",None),
    (u"ti",None),
    (u"tú",None),
    (u"os",None),
    (u"usted",None),
    (u"ustedes",None),
    (u"vos",None),
    (u"vosotras",None),
    (u"vosotros",None),
    (u"contigo",None),
    (u"él",None),
    (u"ella",None),
    (u"ellas",None),
    (u"ello",None),
    (u"ellos",None),
    (u"la","P"),
    (u"las","P"),
    (u"lo","P"),
    (u"los","P"),
    (u"le",None),
    (u"les",None),
    (u"se",None),
    (u"sí","P"),
    (u"consigo",None)
    ]
"""List of pronouns"""

def quantify(analysis):
    """Quantify pronouns."""
     
    freq = analysis.histogram_normalized()
    pairs = []
    for word, pos in PRONOUNS:
        if pos is None:
            pairs.append( (word, freq.get(word, 0.0)) )
        else:
            # For tokens that require disambiguation (e.g., la, las, etc.),
            # we make sure that the token in analysis belongs to the same category
            # as the token in PRONOUNS. 
            # We also check against lower case tokens in the provided text.
            t_pos = analysis.l_word_pos(word)
            if  t_pos != None and t_pos[0] == pos:
                pairs.append( (word, freq.get(word, 0.0)) )

    return dict(pairs)
