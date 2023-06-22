from src.s_translation.gettext import Translation, gettext


# _ = Translation(APP_NAME, 'pl').gettext()
_ = gettext


print(_("Text from EXAMPLE to translate"))
