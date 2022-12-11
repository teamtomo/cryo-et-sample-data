from cryo_et_sample_data.utils import word_wrap_with_line_breaks


def test_word_wrap():
    text = "1234\n\n12345 1234567"
    wrapped_text = word_wrap_with_line_breaks(text, paragraph_width=4)

    assert isinstance(wrapped_text, list)
    assert len(wrapped_text) == 4
    assert wrapped_text[0] == "1234"

    # line breaks are converted to empty strings
    assert wrapped_text[1] == ""

    # long words don't get broken up
    assert wrapped_text[2] == "12345"
    assert wrapped_text[3] == "1234567"
