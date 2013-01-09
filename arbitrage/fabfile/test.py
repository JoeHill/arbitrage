from fabric.api import task
from fabric.operations import *
from fabric.context_managers import lcd

from fabfile import ROOT

@task 
def all( ):
  """Run all the tests (fetchers, preprocessors, algorithms, and postprocessors)"""
  unit()

@task
def unit( ):
  """Test the fetchers."""
  with lcd( ROOT ): 
    local( "nosetests tests/unit.py" ) 
