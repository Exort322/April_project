from setuptools import setup, find_packages


def readme():
  with open('DrunkenJokesLib\DrunkenJokesLib\README.md', 'r') as f:
    return f.read()


setup(
  name='DrunkenJokesLib',
  version='0.0.1',
  author='Drunken',
  author_email='jugger2205@gmail.com',
  description='Best api for jokes and more',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Exort322/April_project',
  packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'python-dateutil>=2.8.2'
    ],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='jokes rofls mems mem prikol drunkenrofl drunkenjokes ',
  project_urls={
    'GitHub': 'https://github.com/Exort322/April_project'
  },
  python_requires='>=3.9'
)