import os
import shutil
import subprocess
from pathlib import Path

from .settings import GETTEXT_DEFAULT_DOMAIN, GETTEXT_DEFAULT_LANGUAGES, GETTEXT_DEFAULT_LOCALE_DIR
from .utils import print_color


class MessageCreatorError(Exception):
    pass


class MessageCreator:
    MESSAGES_PATH_NAME = 'LC_MESSAGES'

    LOCALE_DIR: str
    TEMPLATE_MESSAGE_FILE_NAME: str
    DOMAIN: str
    LANGUAGES: list[str]

    def __init__(self, domain: str = '', languages: list[str] = [], locale_dir: str = '') -> None:
        self.DOMAIN = domain or os.getenv('GETTEXT_DOMAIN', GETTEXT_DEFAULT_DOMAIN)
        self.LANGUAGES = (
            languages
            or [item.strip() for item in os.getenv('GETTEXT_LANGUAGES', '').split(',') if item.strip()]
            or GETTEXT_DEFAULT_LANGUAGES
        )
        self.LOCALE_DIR = locale_dir or os.getenv('GETTEXT_LOCALE_DIR', GETTEXT_DEFAULT_LOCALE_DIR)
        self.TEMPLATE_MESSAGE_FILE_NAME = f'{self.LOCALE_DIR}/{self.DOMAIN}.pot'

    def _get_locale_dir_by_language(self, language: str) -> str:
        return f'{self.LOCALE_DIR}/{language}/{self.MESSAGES_PATH_NAME}'

    def create_message_files(self) -> None:
        """
        Creates a template message file .pot in the dir `{self.LOCALE_DIR}/{self.DOMAIN}.pot`
        Creates message files .po for each language or updates them if existing
        """
        print_color(f"Starting the creation international message files for domain {self.DOMAIN} process:", 'BOLD')
        self._create_directories()
        if self._create_template_message_file():
            self._make_locale_message_files()
            print_color("The gettext message files creation process was SUCCESSFUL", 'BOLD')
        else:
            print_color("Please create at least one message to translate in your code", 'BOLD')

    def _create_directories(self) -> None:
        """
        Creates directories for each language
        """
        for language in self.LANGUAGES:
            path = self._get_locale_dir_by_language(language)
            Path(path).mkdir(parents=True, exist_ok=True)

    def _create_template_message_file(self) -> bool:
        """
        Create new template message file .pot
        """
        print("Creating template message file...")
        args = [
            'bash',
            '-c',
            f'find . -type f -iname "*.py" ! -path "./venv/*" ! -path "./env/*" | xargs xgettext -d {self.DOMAIN} -o {self.TEMPLATE_MESSAGE_FILE_NAME}',
        ]
        try:
            subprocess.run(args)
            with open(self.TEMPLATE_MESSAGE_FILE_NAME) as f:
                content = f.read()
            content = content.replace('charset=CHARSET', 'charset=UTF-8')
            with open(self.TEMPLATE_MESSAGE_FILE_NAME, 'w') as f:
                f.write(content)
            print_color(f"Created template message file: {self.TEMPLATE_MESSAGE_FILE_NAME}", 'OKGREEN')
            return True
        except FileNotFoundError as e:
            print_color(f"Process failed: the executable could not be found.\n{e}", 'ERROR')
        except subprocess.CalledProcessError as e:
            print_color(f"Process failed: return code {e.returncode}\n{e}", 'ERROR')
        except subprocess.TimeoutExpired as e:
            print_color(f"Process timeout expired.\n{e}", "ERROR")
        return False

    def _make_locale_message_files(self) -> None:
        """
        Copy template message files .pot to locale massage file .po for each language
        if there is no .po file for the language.
        Otherwise, update the .po file to new translation contained in the new .pot file
        """
        print("Making locale message files...")
        for language in self.LANGUAGES:
            file_name = self._get_locale_dir_by_language(language) + f'/{self.DOMAIN}.po'
            if not Path(file_name).is_file():
                shutil.copyfile(self.TEMPLATE_MESSAGE_FILE_NAME, file_name)
                print_color(f"Created new locale message file: {file_name}", 'OKGREEN')
            else:
                if not self._update_locale_message_file(file_name):
                    raise MessageCreatorError()

    def _update_locale_message_file(self, file_name: str) -> bool:
        """
        Update the the locale message file .po to new translation contained in the new .pot file
        """
        args = ['msgmerge', '--update', file_name, self.TEMPLATE_MESSAGE_FILE_NAME]
        try:
            subprocess.run(args, capture_output=True, timeout=2, check=True)
            Path(f'{file_name}~').unlink(missing_ok=True)
            print_color(f"Updated locale message file: {file_name}", 'OKGREEN')
            return True
        except FileNotFoundError as e:
            print_color(f"Process failed: the executable could not be found.\n{e}", 'ERROR')
        except subprocess.CalledProcessError as e:
            print_color(f"Process failed: return code {e.returncode}\n{e}", 'ERROR')
        except subprocess.TimeoutExpired as e:
            print_color(f"Process timeout expired.\n{e}", "ERROR")
        return False

    def generate_message_objects(self) -> None:
        """
        Creates locale message object file .mo for each language from file .po,
        which has been filled in with new translations by user
        """
        print_color("Creating locale message object...", 'BOLD')
        for language in self.LANGUAGES:
            locale_directory = self._get_locale_dir_by_language(language)
            mo_file = f'{locale_directory}/{self.DOMAIN}.mo'
            args = ['msgfmt', '-o', mo_file, f'{locale_directory}/{self.DOMAIN}']
            try:
                subprocess.run(args, timeout=2, check=True)
                print_color(f"Generated new message object for language '{language}': {mo_file}", 'OKGREEN')
            except FileNotFoundError as e:
                print_color(f"Process failed: the executable could not be found.\n{e}", 'ERROR')
            except subprocess.CalledProcessError as e:
                print_color(f"Process failed: return code {e.returncode}\n{e}", 'ERROR')
            except subprocess.TimeoutExpired as e:
                print_color(f"Process timeout expired.\n{e}", 'ERROR')
