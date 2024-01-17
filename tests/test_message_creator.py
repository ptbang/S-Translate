from s_translation import MessageCreator

from . import settings
from .base_test_case import MessageCreatorTestBase, TestCaseMeta


class MessageCreatorTest(MessageCreatorTestBase, metaclass=TestCaseMeta):
    TEXT = "Text 1 to translate"
    TRANSLATED_TEXT = "Tekst 1 do przetłumaczenia"

    @classmethod
    def _set_gettext_params(cls) -> None:
        cls.DOMAIN = settings.DOMAIN
        cls.LOCALE_DIR = settings.LOCALE_DIR
        cls.LANGUAGES = settings.LANGUAGES
        cls.LANGUAGE = settings.LANGUAGE

    @classmethod
    def _set_message_creator(cls):
        cls.creator = MessageCreator(cls.DOMAIN, cls.LANGUAGES, cls.LOCALE_DIR)

    @classmethod
    def _get_translated_text_from_file(cls) -> str:
        from .filetest1 import text

        return text
