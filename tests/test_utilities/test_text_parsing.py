from .utilities.text_parsing import convert_to_alphanumeric

def test_convert_to_alphanumeric():
    text1 = "me & you!"
    assert convert_to_alphanumeric(text1) == "meyou"
    text2 = "me & you!"
    assert convert_to_alphanumeric(text2, include_spaces = True) == "me  you"
