rm ./dist/*
python3.10 -m build
twine upload --repository gitea dist/*
twine upload --repository pypi dist/*