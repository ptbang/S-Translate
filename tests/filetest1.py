from s_translation.gettext import Translation

from . import settings

_ = Translation(settings.DOMAIN, settings.LANGUAGE, settings.LOCALE_DIR).gettext

text = _("Text 1 to translate")
