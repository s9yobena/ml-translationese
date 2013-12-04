# -*- coding: utf-8 -*-

"""\
This hypothesis checks whether pronouns taken from
`http://nlp.lsi.upc.edu/freeling/doc/tagsets/tagset-es.html#pronombres` alone
can yield a high classification accuracy. Each pronoun in the corpus is a
feature, whose value is the normalized frequency of its occurrences in the
chunk.
"""

PRONOUNS = [
 "yo",
 "me",
 "mí",
 "nos",
 "nosotras",
 "nosotros",
 "conmigo",
 "te",
 "ti",
 "tú",
 "os",
 "usted",
 "ustedes",
 "vos",
 "vosotras",
 "vosotros",
 "contigo",
 "él",
 "ella",
 "ellas",
 "ello",
 "ellos",
 "la",
 "las",
 "lo",
 "los",
 "le",
 "les",
 "se",
 "sí",
 "consigo",
]
"""List of pronouns"""

def quantify(analysis):
    """Quantify pronouns."""
    freq = analysis.histogram_normalized()
    pairs = [ (word, freq.get(word, 0.0)) for word in PRONOUNS ]
    return dict(pairs)
