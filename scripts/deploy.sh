python -m virtualenv env
source env/bin/activate
pip install twine
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
