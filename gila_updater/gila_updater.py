import json
import re
import subprocess

from git import Repo


class GilaUpdater:

    def __init__(self):
        self.repo_url = "https://github.com/fran-00/gila.git"
        self.local_dir = "storage/cloned_repo"
