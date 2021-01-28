"""
this is the unit test of input_from_string_bracket_form.
"""
from nlp_platform.plug_in.input.ntree_from_string_bracket_form import input_ntree_from_string_bracket_form
from nlp_platform.plug_in.output.ntree_to_string_bracket_form import output_ntree_to_string_bracket_form

ntree = input_ntree_from_string_bracket_form('(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))')
out = output_ntree_to_string_bracket_form(ntree)
print(out)
