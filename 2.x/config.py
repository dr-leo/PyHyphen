# This file contains default config info for downloading and installing dictionaries
# The template placeholders are filled by setup.py.
import os

current_dir = os.path.abspath(os.path.dirname(__file__))


# Local path for dictionaries
default_dict_path = current_dir

# path for the metadata file
default_dict_info_path = current_dir

# URL of the repository for dictionaries
# Change this if you want to download dictionaries from somewhere else by default.
# Note that you can also specify the repository individually
# when calling hyphen.dictools.install.
default_repository = u'http://cgit.freedesktop.org/libreoffice/dictionaries/plain/'

# Country and language codes: These will be appended to the default_repos path
languages = set(('af_ZA', 'an_ES', 'ar', 'be_BY', 'bg_BG',
'bn_BD', 'br_FR', 'ca', 'cs_CZ', 'da_DK', 'de',
'el_GR', 'en', 'es_ES', 'et_EE', 'fr_FR', 'gd_GB', 'gl',
'gu_IN', 'he_IL', 'hi_IN', 'hr_HR', 'hu_HU', 'it_IT', 'ku_TR',
'lt_LT', 'lv_LV', 'ne_NP', 'nl_NL', 'no', 'oc_FR', 'pl_PL',
'prj', 'pt_BR', 'pt_PT', 'ro', 'ru_RU', 'si_LK', 'sk_SK',
'sl_SI', 'sr', 'sv_SE', 'sw_TZ',
'te_IN', 'th_TH', 'uk_UA', 'zu_ZA'))
