from utils.color import ColoredStr


def test_colored_str():
    ColoredStr("Hello, World!", foreground=(255, 0, 0), background="ff0000")
    ColoredStr("Hello, World!", foreground="ff0000", background=(255, 0, 0))
    ColoredStr("Hello, World!", foreground=(255, 0, 0))
    ColoredStr("Hello, World!", background="ff0000")
    ColoredStr("Hello, World!")
