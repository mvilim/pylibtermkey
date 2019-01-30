pip install twine
echo test twine password
echo $TWINE_PASSWORD
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
