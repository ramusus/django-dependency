#!/usr/bin/env python

from distutils.core import setup

setup(name='django-dependency',
      version='1.0',
      description='Django app to help manage external dependencies',
      author='Caktus Consulting Group, LLC',
      author_email='solutions@caktusgroup.com',
      url='https://github.com/ramusus/django-dependency/',
      packages=['deps', 'deps.management', 'deps.management.commands'],
      scripts=['scripts/create_deps.py']
)

