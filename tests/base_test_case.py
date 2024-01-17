import fileinput
import shutil
import sys
import types
from pathlib import Path
from unittest import TestCase

from s_translation import MessageCreator
from s_translation.utils.print_color import print_color


class TestCaseMeta(type):
    def __new__(cls, name: str, bases: tuple[type], dct: dict) -> type:
        if 'Base' not in name:
            for base in bases:
                for key, value in base.__dict__.items():
                    if key.startswith('_test_') and isinstance(value, types.FunctionType) and key[1:] not in dct:
                        dct[key[1:]] = value
        return super().__new__(cls, name, bases, dct)


class MessageCreatorTestBase(TestCase):
    DOMAIN: str
    LOCALE_DIR: str
    LANGUAGES: list[str]
    LANGUAGE: str
    TEXT: str
    TRANSLATED_TEXT: str
    creator: MessageCreator

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._set_gettext_params()
        cls._set_message_creator()
        cls._create_gettext_messages()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._remove_locale_dir()

    @classmethod
    def _set_gettext_params(cls) -> None:
        """Set class properties DOMAIN, LOCALE_DIR, LANGUAGES, LANGUAGE"""
        raise NotImplementedError
    

    @classmethod
    def _set_message_creator(cls) -> None:
        raise NotImplementedError

    @classmethod
    def _create_gettext_messages(cls) -> None:
        cls.creator.create_message_files()
        cls._fill_translation()
        cls.creator.generate_message_objects()

    def _test_all(self) -> None:
        # self.creator.create_message_files()
        self.assertTrue(Path(self._get_template_message_file()).is_file())
        with open(self._get_template_message_file(), 'r') as f:
            file_content = f.read()
        self.assertTrue("Text 1 to translate" in file_content)
        self.assertTrue("Text 2 to translate" in file_content)
        self.assertTrue("Text 3 to translate" in file_content)
        for language in self.LANGUAGES:
            message_file_name = self._get_message_file_by_language(language)
            self.assertTrue(Path(message_file_name).is_file())
            with open(message_file_name, 'r') as f:
                file_content = f.read()
            self.assertTrue("Text 1 to translate" in file_content)
            self.assertTrue("Text 2 to translate" in file_content)
            self.assertTrue("Text 3 to translate" in file_content)

        # self._fill_translation()
        # self.creator.generate_message_objects()
        for language in self.LANGUAGES:
            self.assertTrue(Path(self._get_message_object_file_by_language(language)).is_file())

        self.assertEqual(self._get_translated_text_from_file(), self.TRANSLATED_TEXT)

        # self._remove_locale_dir()

    def _get_template_message_file(self) -> str:
        return f'{self.LOCALE_DIR}/{self.DOMAIN}.pot'

    @classmethod
    def _get_message_file_by_language(cls, language: str) -> str:
        return cls._get_locale_dir_by_language(language) + f'/{cls.DOMAIN}.po'

    @classmethod
    def _get_locale_dir_by_language(cls, language: str) -> str:
        return f'{cls.LOCALE_DIR}/{language}/{cls.creator.MESSAGES_PATH_NAME}'

    def _get_message_object_file_by_language(self, language: str) -> str:
        return self._get_locale_dir_by_language(language) + f'/{self.DOMAIN}.mo'

    @classmethod
    def _remove_locale_dir(cls) -> None:
        """
        Be careful when using this function!!!
        First, check if your LOCAL_DIR is correct!!!
        """
        print_color(f"Deleting LOCAL_DIR: {cls.LOCALE_DIR}...", 'WARNING')
        shutil.rmtree(cls.LOCALE_DIR)

    @classmethod
    def _fill_translation(cls) -> None:
        to_fill = False
        for line in fileinput.input(cls._get_message_file_by_language(cls.LANGUAGE), inplace=True):
            if to_fill:
                line = line.replace('""', f'"{cls.TRANSLATED_TEXT}"')
                to_fill = False

            if cls.TEXT in line:
                to_fill = True
            sys.stdout.write(line)

    @classmethod
    def _get_translated_text_from_file(cls) -> str:
        raise NotImplementedError
