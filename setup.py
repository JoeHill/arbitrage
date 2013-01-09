try:
  from setuptools import setup, find_packages
except ImportError:
  import distribute_setup
  distribute_setup.use_setuptools()
  from setuptools import setup, find_packages

setup(
  name='arbitrage',
  version='0.0.1',
  packages=find_packages(),
  author='Andrew Kelleher',
  author_email='akellehe@gmail.com',
  description='A package for assembling coherent data from news sources.'
)
