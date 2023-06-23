class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


styles = list(BColors.__dict__.keys())
styles.remove('ENDC')


def print_color(msg: str, style: str = '') -> None:
    if style not in styles:
        style = ''
    style_start = getattr(BColors, style, '')
    style_end = BColors.ENDC if style else ''
    print(f"{style_start}{msg}{style_end}")
