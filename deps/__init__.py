import settings
import os
import sys
import shutil
import urlparse

class MissingDependency(Exception):
    pass

class VersionControl(object):

    def __init__(self, url, app_dir, app_name=None, root=None):
        self.url = url
        self.root = root or settings.DEPENDENCY_ROOT

        self.project_name = app_dir
        self.app_name = app_name or self.project_name

        self.python_path = os.path.join(
            self.root,
            self.project_name,
        )
        self.path = os.path.join(
            self.root,
            self.project_name,
            self.app_name,
        )

    def __repr__(self):
        return "<VersionControl: %s>" % self.app_name

    def add_to_python_path(self, position):
        if not os.path.exists(self.path):
            raise MissingDependency('%s does not exist.  Run "./manage.py up" to retrieve this dependency' % self.app_name)
        sys.path.insert(position, self.python_path)

    def checkout(self, command):
        self.log('checking out %s:%s' % (self.type, self.app_name))
        os.system(command)

    def update(self, command, change_dir=False):
        self.log('updating %s:%s' % (self.type, self.app_name))
        if os.path.exists(self.python_path):
            if change_dir:
                os.chdir(self.python_path)
            os.system(command)
        else:
            self.checkout()

    def status(self, command, change_dir=False):
        self.log('status %s:%s' % (self.type, self.app_name))
        if change_dir:
            os.chdir(self.python_path)
        os.system(command)

    def log(self, message):
        message = ' -> ' + message
        print message

class HG(VersionControl):
    type = 'hg'
    def checkout(self):
        super(HG, self).checkout('hg clone %s %s' % (self.url, self.python_path))
    def update(self):
        super(HG, self).update('hg update', change_dir=True)
    def status(self):
        super(HG, self).status('hg status %s' % self.python_path)

class SVN(VersionControl):
    type = 'svn'
    def checkout(self):
        super(SVN, self).checkout('svn co %s %s' % (self.url, self.python_path))
    def update(self):
        super(SVN, self).update('svn up %s' % self.python_path)
    def status(self):
        super(SVN, self).status('svn status %s' % self.python_path)

class GIT(VersionControl):
    type = 'git'
    def checkout(self):
        super(GIT, self).checkout('git clone %s %s' % (self.url, self.python_path))
    def update(self):
        super(GIT, self).update('git pull %s master' % self.url, change_dir=True)
    def status(self):
        super(GIT, self).status('git status .', change_dir=True)

class BZR(VersionControl):
    type = 'bzr'
    def checkout(self):
        super(BZR, self).checkout('bzr branch %s %s' % (self.url, self.python_path))
    def update(self):
        super(BZR, self).update('bzr update %s' % self.python_path)
    def status(self):
        super(BZR, self).status('bzr status %s' % self.python_path)

def add_all_to_path(settings, auto_update=False, position=1):
    for dependency in settings.DEPENDENCIES:
        try:
            dependency.add_to_python_path(position)
        except MissingDependency:
            if auto_update:
                dependency.up()
            else:
                raise
            dependency.add_to_python_path(position)
