from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name='django-rest-framework-condition',
      version='0.1.0',
      packages=find_packages(),
      author='jozo',
      author_email='hi@jozo.io',
      description='Decorators @condition, @last_modified and @etag for Django Rest Framework',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/jozo/django-rest-framework-condition',
      install_requires=[
          'Django'
      ],
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
      ],
      )
