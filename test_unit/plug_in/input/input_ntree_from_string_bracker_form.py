"""
this is the unit test of input_from_string_bracket_form.
"""
from nlp_plantform.plug_in.input.ntree_from_string_bracket_form import input_ntree_from_string_bracket_form

r = input_ntree_from_string_bracket_form('(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))')
r.draw()
