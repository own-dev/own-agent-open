"""
Constants for utils package
"""
import os
from http import HTTPStatus

from utils import logger

# === HTTP Headers ===
# To avoid 403 error code
HTTP_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# === Agents path ===
AGENTS_PATH = os.environ['OWN_AGENTS_PATH']
AGENT_UTILS_NAME = 'agents_utils'

TIMEOUT_INTERVAL = 10

SUCCESS_CODE = HTTPStatus.OK
BAD_REQUEST_CODE = HTTPStatus.BAD_REQUEST
NO_CONTENT_CODE = HTTPStatus.NO_CONTENT

MAX_INT = 1e20

ENGLISH = 'en'

# === IBM NER labels ===
# doc: https://console.bluemix.net/docs/services/natural-language-understanding/entity-types-v1.html
LOCATION_IBM_LABEL = 'Location'
ORGANIZATION_IBM_LABEL = 'Organization'
PERSON_IBM_LABEL = 'Person'
JOB_TITLE_IBM_LABEL = 'JobTitle'
COMPANY_IBM_LABEL = 'Company'

IP_ADDRESS_KEY = 'ip'
MESSAGE_KEY = 'message'
AGENT_NUMBER_KEY = 'agent_number'
NUMBER_OF_TASKS_KEY = 'num_tasks'

DOWNLOADS_DIR = 'downloads'
MAX_NUMBER_OF_TOPIC_SYMBOLS_IN_FILENAME = 30

try:
    AGENTS_PATH = os.environ['OWN_AGENTS_PATH']
    # TODO: Check if paths below exist
    ACTUAL_AGENTS_PATH = os.path.join(AGENTS_PATH, 'agents')
except KeyError as e:
    logger.exception(AGENT_UTILS_NAME, f'OWN_AGENTS_PATH is undefined. Error message: {e}')

MARKETS = {'ar': 'ar-sa',
           'da': 'da-dk',
           'de': 'de-de',
           'en': 'en-us',
           'es': 'es-es',
           'fi': 'fi-fi',
           'fr': 'fr-fr',
           'it': 'it-it',
           'ja': 'ja-jp',
           'ko': 'ko-kr',
           'nl': 'nl-nl',
           'no': 'no-no',
           'pl': 'pl-pl',
           'pt': 'pt-pt',
           'ru': 'ru-ru',
           'sv': 'sv-se',
           'tr': 'tr-tr',
           'zh': 'zh-cn'}

USER_DEFINED_MARKETS = {'Worldwide': 'en-ww',
                        'Arabic': 'ar-sa',
                        'Danish': 'da-dk',
                        'German-Austria': 'de-at',
                        'German-Switzerland': 'de-ch',
                        'German-Germany': 'de-de',
                        'English-Australia': 'en-au',
                        'English-Canada': 'en-ca',
                        'English-UK': 'en-gb',
                        'English-Indonesia': 'en-id',
                        'English-Ireland': 'en-ie',
                        'English-India': 'en-in',
                        'English-Malaysia': 'en-my',
                        'English-Mexico': 'en-mx',
                        'English-New Zealand': 'en-nz',
                        'English-Philippines': 'en-ph',
                        'English-United States': 'en-us',
                        'English-South Africa': 'en-za',
                        'Spanish-Argentina': 'es-ar',
                        'Spanish-Chile': 'es-cl',
                        'Spanish-Mexico': 'es-mx',
                        'Spanish-Spain': 'es-es',
                        'Spanish-United States': 'es-us',
                        'Finnish': 'fi-fi',
                        'French-Belgium': 'fr-be',
                        'French-Canada': 'fr-ca',
                        'French-Switzerland': 'fr-ch',
                        'French-France': 'fr-fr',
                        'Italian': 'it-it',
                        'Japanese': 'ja-jp',
                        'Korean': 'ko-kr',
                        'Dutch-Belgium': 'nl-be',
                        'Dutch-Netherlands': 'nl-nl',
                        'Norwegian': 'no-no',
                        'Polish': 'pl-pl',
                        'Portuguese-Portugal': 'pt-pt',
                        'Portuguese-Brazil': 'pt-br',
                        'Russian': 'ru-ru',
                        'Swedish': 'sv-se',
                        'Turkish': 'tr-tr',
                        'Chinese': 'zh-cn',
                        'Traditional Chinese-Hong Kong SAR': 'zh-hk',
                        'Traditional Chinese-Taiwan': 'zh-tw'}
UNDEFINED_LANGUAGE = 'und'

MARKET_LANGUAGES = {'ar-sa': 'ar',
                    'da-dk': 'da',
                    'de-at': 'de',
                    'de-ch': 'de',
                    'de-de': 'de',
                    'en-au': 'en',
                    'en-ca': 'en',
                    'en-gb': 'en',
                    'en-id': 'en',
                    'en-ie': 'en',
                    'en-in': 'en',
                    'en-my': 'en',
                    'en-mx': 'en',
                    'en-nz': 'en',
                    'en-ph': 'en',
                    'en-us': 'en',
                    'en-za': 'en',
                    'es-ar': 'es',
                    'es-cl': 'es',
                    'es-mx': 'es',
                    'es-es': 'es',
                    'es-us': 'es',
                    'fi-fi': 'fi',
                    'fr-be': 'fr',
                    'fr-ca': 'fr',
                    'fr-ch': 'fr',
                    'fr-fr': 'fr',
                    'it-it': 'it',
                    'ja-jp': 'ja',
                    'ko-kr': 'ko',
                    'nl-be': 'nl',
                    'nl-nl': 'nl',
                    'no-no': 'no',
                    'pl-pl': 'pl',
                    'pt-pt': 'pt',
                    'pt-br': 'pt',
                    'ru-ru': 'ru',
                    'sv-se': 'sv',
                    'tr-tr': 'tr',
                    'zh-cn': 'zh-cn',
                    'zh-hk': 'zh-tw',
                    'zh-tw': 'zh-tw',
                    'en-ww': 'en'}

MARKET_TRANSLATE_LANGUAGES = {'ar': 'ar',
                              'da': 'da',
                              'de': 'de',
                              'en': 'en',
                              'es': 'es',
                              'fi': 'fi',
                              'fr': 'fr',
                              'it': 'it',
                              'ja': 'ja',
                              'ko': 'ko',
                              'nl': 'nl',
                              'no': 'no',
                              'pl': 'pl',
                              'pt': 'pt',
                              'ru': 'ru',
                              'sv': 'sv',
                              'tr': 'tr',
                              'zh-cn': 'zh',
                              'zh-tw': 'zh-TW'}

TRANSLATE_LANGUAGES = {'Afrikaans': 'af',
                       'Albanian': 'sq',
                       'Amharic': 'am',
                       'Arabic': 'ar',
                       'Armenian': 'hy',
                       'Azerbaijani': 'az',
                       'Basque': 'eu',
                       'Belarusian': 'be',
                       'Bengali': 'bn',
                       'Bosnian': 'bs',
                       'Bulgarian': 'bg',
                       'Catalan': 'ca',
                       'Cebuano': 'ceb',
                       'Chinese (Simplified)': 'zh-CN',
                       'Chinese (Traditional)': 'zh-TW',
                       'Corsican': 'co',
                       'Croatian': 'hr',
                       'Czech': 'cs',
                       'Danish': 'da',
                       'Dutch': 'nl',
                       'English': 'en',
                       'English (incl. smart summaries)': 'en',
                       'Esperanto': 'eo',
                       'Estonian': 'et',
                       'Finnish': 'fi',
                       'French': 'fr',
                       'Frisian': 'fy',
                       'Galician': 'gl',
                       'Georgian': 'ka',
                       'German': 'de',
                       'Greek': 'el',
                       'Gujarati': 'gu',
                       'Haitian Creole': 'ht',
                       'Hausa': 'ha',
                       'Hawaiian': 'haw',
                       'Hebrew': 'he**',
                       'Hindi': 'hi',
                       'Hmong': 'hmn',
                       'Hungarian': 'hu',
                       'Icelandic': 'is',
                       'Igbo': 'ig',
                       'Indonesian': 'id',
                       'Irish': 'ga',
                       'Italian': 'it',
                       'Japanese': 'ja',
                       'Javanese': 'jw',
                       'Kannada': 'kn',
                       'Kazakh': 'kk',
                       'Khmer': 'km',
                       'Korean': 'ko',
                       'Kurdish': 'ku',
                       'Kyrgyz': 'ky',
                       'Lao': 'lo',
                       'Latin': 'la',
                       'Latvian': 'lv',
                       'Lithuanian': 'lt',
                       'Luxembourgish': 'lb',
                       'Macedonian': 'mk',
                       'Malagasy': 'mg',
                       'Malay': 'ms',
                       'Malayalam': 'ml',
                       'Maltese': 'mt',
                       'Maori': 'mi',
                       'Marathi': 'mr',
                       'Mongolian': 'mn',
                       'Myanmar (Burmese)': 'my',
                       'Nepali': 'ne',
                       'Norwegian': 'no',
                       'Nyanja (Chichewa)': 'ny',
                       'Pashto': 'ps',
                       'Persian': 'fa',
                       'Polish': 'pl',
                       'Portuguese (Portugal, Brazil)': 'pt',
                       'Punjabi': 'pa',
                       'Romanian': 'ro',
                       'Russian': 'ru',
                       'Samoan': 'sm',
                       'Scots Gaelic': 'gd',
                       'Serbian': 'sr',
                       'Sesotho': 'st',
                       'Shona': 'sn',
                       'Sindhi': 'sd',
                       'Sinhala (Sinhalese)': 'si',
                       'Slovak': 'sk',
                       'Slovenian': 'sl',
                       'Somali': 'so',
                       'Spanish': 'es',
                       'Sundanese': 'su',
                       'Swahili': 'sw',
                       'Swedish': 'sv',
                       'Tagalog (Filipino)': 'tl',
                       'Tajik': 'tg',
                       'Tamil': 'ta',
                       'Telugu': 'te',
                       'Thai': 'th',
                       'Turkish': 'tr',
                       'Ukrainian': 'uk',
                       'Urdu': 'ur',
                       'Uzbek': 'uz',
                       'Vietnamese': 'vi',
                       'Welsh': 'cy',
                       'Xhosa': 'xh',
                       'Yiddish': 'yi',
                       'Yoruba': 'yo',
                       'Zulu': 'zu'}

# For keywords extraction

DEFAULT_NUM_CITED = 10
DEFAULT_NUM_RECENT = 5
DEFAULT_INCLUDE_SPRINGER = False
DEFAULT_NUM_OF_SENT = 7
DEFAULT_NUM_OF_WORDS_TO_RECOGNIZE_LANGUAGE = 10
MIN_ACCEPTABLE_KW_NUM = 5
MIN_ACCEPTABLE_ART_NUM = 2
SINGLE_WORD = 1
DEFAULT_KW_WEIGHT = 1
DEFAULT_KW_WEIGHT_FIELD_OF_STUDY = 1.05
KW_THRESHOLD = 0.2

ART_ID_KEY = 'id'
ART_DOI_KEY = 'doi'
ART_PII_KEY = 'pii'
ART_EID_KEY = 'eid'
ART_ISSN_KEY = 'issn'
ART_ISBN_KEY = 'isbn'
ART_SID_KEY = 'sid'
ART_TITLE_KEY = 'title'
ART_NAME_KEY = 'name'
ART_DATE_KEY = 'date'
ART_AUTHORS_KEY = 'authors'
ART_KEYWORDS_KEY = 'keywords'
ART_PROCEEDED_KW_KEY = 'proceeded_keywords'
ART_URL_KEY = 'url'
ART_CITED_NUM_KEY = 'cited_num'
ART_ABSTRACT_KEY = 'abstract'
ART_JOURNAL_NAME_KEY = 'journal_name'
ART_JOURNAL_ISSUE_KEY = 'journal_issue'
ART_JOURNAL_VOLUME_KEY = 'journal_volume'
ART_START_PAGE_KEY = 'start_page'
ART_END_PAGE_KEY = 'end_page'

KW_TOPIC_KEY = 'topic'
KW_PAPERS_KEY = 'papers'
KW_FROM_YEAR_KEY = 'from_year'
KW_UNTIL_YEAR_KEY = 'until_year'
KW_KEYWORD_KEY = 'keyword'

MS_FIELD_OF_STUDY_KEY = 'field_of_study'