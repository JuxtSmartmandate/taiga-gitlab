import os

GITLAB_PERSONAL_ACCESS_TOKEN = ""
GITLAB_URL = ""

try:
    from local_config import *
except ImportError:
    pass
