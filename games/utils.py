def wrap(text, width):
    """
    Splits the text into lines of roughly the same width.

    >>> wrap('example', 3)
    ['exa', 'mpl', 'e']
    """
    return [text[i:i+width] for i in range(0, len(text), width)]
