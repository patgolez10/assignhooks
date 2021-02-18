rm -rf dist build assignhooks.egg-info
find . -name '*.pyc' | xargs rm -f
find . -name '__pycache__' | xargs rm -rf
