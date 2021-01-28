"""
this is the unit test of input_from_string_bracket_form.
"""
from nlp_platform.plug_in.input.ntree_from_string_plaintext_form import input_from_string_plaintext_form

r = input_from_string_plaintext_form("To begin, log in with your user ID and password. If you are unsure about whether or not you have an account, or have forgotten your password, go to the Reset Password screen.")
r.draw()
