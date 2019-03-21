from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name='django-rest-framework-condition',
      version='0.1.0',
      packages=find_packages(),
      author='jozo',
      author_email='hi@jozo.io',
      description='Use decorators condition, last_modified and etag on ViewSet and APIView from Django Rest Framework',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/jozo/django-rest-framework-condition',
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
      ],
      )
