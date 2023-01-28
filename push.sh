rm ./dist/*
python3.10 setup.py sdist
# twine upload --repository gitea dist/*
twine upload --repository pypi dist/*
