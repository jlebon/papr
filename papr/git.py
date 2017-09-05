#!/usr/bin/env python3

import os
import subprocess


class Git:

    '''
        Simple git helper class which remembers the context directory.
    '''

    def __init__(self, dir, repo_url):
        self.dir = dir
        self.repo_url = repo_url

    def update(self):
        # use .git here in case the clone fails
        if not os.path.isdir(os.path.join(self.dir, ".git")):
            os.makedirs(self.dir, exist_ok=True)
            self.clone()
        else:
            self.fetch()

    def cmd(self, *args):
        return subprocess.run(['git', '-C', self.dir] + list(args), check=True)

    def clone(self):
        return self.cmd("clone", self.repo_url, ".")

    def fetch(self, ref=None):
        args = ["fetch", "origin"]
        if ref is not None:
            args.append(ref)
        return self.cmd(*args)

    def get_rev(self, ref):
        p = subprocess.run(['git', '-C', self.dir, "rev-parse", ref],
                           check=True, stdout=subprocess.PIPE)
        return p.stdout.strip().decode('ascii')

    def get_head(self):
        return self.get_rev("HEAD")

    def checkout(self, ref):
        return self.cmd("checkout", ref)
