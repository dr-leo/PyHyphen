# Test suite for PyHyphen. A test consists of hyphenating all words of a text file using
# specified dictionaries which will be installed on the fly, if necessary.
#
# To add a test, see the instructions and example at the end of this file above the clean up code..


import codecs, logging, os
from hyphen import hyphenator
from hyphen.dictools import *


# Set up logging to the console and the log file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename ='hyphen_test.log')

console = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class wordlist:
    def __init__(self, filename, enc, languages):
        self.filename = filename
        self.encoding = enc
        self.languages = languages
        self.check_dictionaries()
        self.prepare_wordlist()
        self.hyphenate()


    def check_dictionaries(self):
        for lang in self.languages:
            #if the required dictionary is neither found in the default dir nor here, install it here.
            if not (is_installed(lang) or is_installed(lang, '.')):
                logging.info('Installing dictionary %s...', lang)
                install(lang, '.')
                logging.info('Done.')


    def prepare_wordlist(self):
        logging.info('Loading %s...', self.filename)
        f = codecs.open('/'.join(('input', self.filename)), 'r', self.encoding)
        raw_words = f.read().split()
        f.close()
        self.words = list(set(raw_words))
        logging.info('Consolidated list contains %d words.', len(self.words))


    def hyphenate(self):
        for lang in self.languages:
            logging.info('Hyphenating %s with dictionary %s', self.filename, lang)
            if is_installed(lang): h = hyphenator(lang)
            else:
                h = hyphenator(lang, '.')
            output_filename = ''.join(('output/', lang, '.',  self.filename))
            f = codecs.open(output_filename, 'w', self.encoding)
            logging.info('Writing to output file %s...', output_filename)
            f.writelines('Output file created by hyphen_test.\nFormat: word * pairs.\n==========\n')
            for w in self.words:
                pairs_str = ' / '.join(['- '.join((p[0], p[1])) for p in h.pairs(w)])
                f.write(' * '.join((w, pairs_str)))
                f.write('.\n')
            f.write('*** Word list completed. ***')
            f.close()
            logging.info('Finished %s.', output_filename)

# Create the output dir, if it doesn't already exist:
if not os.path.exists('output'):
    logging.info('Creating output directory...')
    os.mkdir('output')

# Each of the following  instances of wordlist hyphenates a word list with one or more
# dictionaries. To extend the test suite, copy your word list into the input
# subdirectory, choose the encoding and dictionaries you may work with and add the resulting
# command hereunder.


# This test runs out of the box.
wordlist('top10000en.txt', 'ascii', ['en_US'])



# clean. On my good old Win2000 machine the attempt to remove the .dic file
# caused an error as allegedly the file was still used by another process.
# This is surprising as the .dic file should be closed during successful instantiation
# of a hyphenator object (after loading the dictionary).
# Under Linux, this error did not occur. I therefore believe the error
# is due to some interesting feature of Windows 2000.

for d in list_installed('.'):
    logging.info('Uninstalling dictionary %s.', d)
    uninstall(d, '.')
logging.info('Test suite completed.')


