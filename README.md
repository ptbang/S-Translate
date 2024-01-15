# S-Translation

A package for easily using gettext in python projects

## Requirements

- python 3.10
- python package `python-dotenv` (`pip install python-dotenv`)


## Getting started


### With .env file
1. First, create a new `.env` file in your project, eg:

    ```text
    GETTEXT_DOMAIN=myapp
    LOCALE_DIR=locales  # => directory inside your project base dir to store the gettext translations
    GETTEXT_LANGUAGES='pl,en'
    GETTEXT_LANGUAGE=pl
    ```

2. Load environment variables from `.env` file to use above environment variables:

    ```python
    from dotenv import load_dotenv

    load_dotenv()
    ```

3. Create translations files:

    ```python
    from s_translation import MessageCreator

    creator = MessageCreator()
    creator.create_message_files()
    ```

4. Next, put your translations to the created files in the previous step eg. `./locales/{language}/LC_MESSAGES/myapp.po`.

5. So, now generate gettext message object files by:

    ```python
    from s_translation import MessageCreator

    creator = MessageCreator()
    creator.generate_message_objects()
    ```

Now, your gettext translation is ready to use.

```python
from s_translation import gettext as _

print(_("Hello, world"))
```


### Without .env file

1. Create translations files:

    ```python
    from s_translation import MessageCreator

    creator = MessageCreator(domain='myapp', languages=['en', 'pl'], locale_dir='locales')
    creator.create_message_files()
    ```

2. Next, put your translations to the created files in the previous step `./locales/{language}/LC_MESSAGES/myapp.po` e.g. `./locales/pl/LC_MESSAGES/myapp.po`

3. So, now generate gettext message object files by:

    ```python
    from s_translation import MessageCreator

    creator = MessageCreator(domain='myapp', languages=['en', 'pl'], locale_dir='locales')
    creator.generate_message_objects()
    ```


Now, your gettext translation is ready to use.

```python
from s_translation import Translation

_ = Translation(domain='myapp', language='pl', locale_dir='locales').gettext

print(_("Hello, world"))
```
