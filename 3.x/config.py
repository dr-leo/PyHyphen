# This file contains default config info for downloading and installing dictionaries
# The template placeholders are filled by setup.py.



# Local path for dictionaries
default_dict_path = '$path'

# URL of the repository for dictionaries
default_repository = '$repo'

# Language names to append to the repository URL. Catch error occurring on first import
try:
    suffixes = eval("$suff")
except SyntaxError: pass

