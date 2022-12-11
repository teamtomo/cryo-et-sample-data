import textwrap
from typing import List


def word_wrap_with_line_breaks(
    words_to_wrap: str,
    paragraph_width: int = 70,
) -> List[str]:
    """Word wrap a string while preserving existing line breaks.

    Parameters
    ----------
    words_to_wrap : str
        The line to wrap.
    paragraph_width : int
        The number of characters wide the resulting paragraph should be.

    Returns
    -------
    wrapped_words : List[str]
        The input string broken up by the specified line width.
        Each element in the list is one one. wrapped_words can
        be combined into a single string use `"\n".join(wrapped_words)`.
    """
    wrapped_words = []
    for line in words_to_wrap.splitlines(True):
        if line == "\n":
            wrapped_words.append("")
        else:
            wrapped_words += textwrap.wrap(
                line,
                paragraph_width,
                break_long_words=False,
                replace_whitespace=False,
            )
    return wrapped_words
