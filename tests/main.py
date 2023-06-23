import sys
from os.path import dirname
from pathlib import Path

from dotenv import load_dotenv

sys.path.append(dirname(Path(__name__).absolute()))

load_dotenv()


# from tests import APP_NAME, LANGUAGES

from s_translation.gettext import Translation, gettext
from s_translation.message_creator import MessageCreator

# _ = Translation(APP_NAME, 'pl').gettext()
_ = gettext


def create_gettext_translation():
    creator = MessageCreator()
    creator.create_message_files()
    # creator.generate_message_objects()


if __name__ == '__main__':
    create_gettext_translation()
    # print(locale.getlocale())
    # print(os.getenv('LANG'))

    # for name, value in os.environ.items():
    #     print("{0}: {1}".format(name, value))

    # print(os.getenv('LANGI'))

    print(_('Hello, world'))
