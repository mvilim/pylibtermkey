# temporary fix for https://github.com/joerick/cibuildwheel/issues/122
# pip install cibuildwheel==0.10.0
pip install git+https://github.com/YannickJadoul/cibuildwheel.git@pip-19-stalling-workaround
cibuildwheel --output-dir dist

# only create the source distribution from linux, so that we don't try to upload it twice
if [ "$TRAVIS_OS_NAME" = "linux" ]
then
    python setup.py sdist --dist-dir dist
fi
