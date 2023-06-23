import gettext as base_gettext
import os

from .settings import DEFAULT_LANGUAGE, GETTEXT_DEFAULT_DOMAIN, GETTEXT_DEFAULT_LOCALE_DIR


class Translation:
    LOCALE_DIR: str
    DOMAIN: str
    LANGUAGE: str

    def __init__(self, domain: str = '', language_code: str = '', locale_dir: str = '') -> None:
        self.DOMAIN = domain or os.environ.get('GETTEXT_DOMAIN', GETTEXT_DEFAULT_DOMAIN)
        self.LANGUAGE = language_code or os.environ.get('GETTEXT_LANGUAGE', DEFAULT_LANGUAGE)
        self.LOCALE_DIR = locale_dir or os.getenv('GETTEXT_LOCALE_DIR', GETTEXT_DEFAULT_LOCALE_DIR)

    def gettext(self, message: str) -> str:
        language_translation = base_gettext.translation(self.DOMAIN, self.LOCALE_DIR, languages=[self.LANGUAGE])
        return language_translation.gettext(message)


gettext = Translation().gettext
