import os

from dotenv import load_dotenv

from s_translation import MessageCreator

from .base_test_case import MessageCreatorTestBase, TestCaseMeta

load_dotenv()


class MessageCreatorWithEnvTest(MessageCreatorTestBase, metaclass=TestCaseMeta):
    TEXT = "Text 2 to translate"
    TRANSLATED_TEXT = "Tekst 2 do przetłumaczenia"

    @classmethod
    def _set_gettext_params(cls) -> None:
        cls.DOMAIN = os.getenv("GETTEXT_DOMAIN")  # type: ignore
        cls.LOCALE_DIR = os.getenv("GETTEXT_LOCALE_DIR")  # type: ignore
        cls.LANGUAGES = [item.strip() for item in os.getenv('GETTEXT_LANGUAGES', '').split(',') if item.strip()]
        cls.LANGUAGE = os.getenv('GETTEXT_LANGUAGE')  # type: ignore

    @classmethod
    def _set_message_creator(cls):
        cls.creator = MessageCreator()

    @classmethod
    def _get_translated_text_from_file(cls) -> str:
        from .filetest2 import text

        return text
