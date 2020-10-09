set -e -x

CIBUILDWHEEL_VERSION=1.5.5

if [ "$TRAVIS_OS_NAME" = "linux" ]; then
    pip install cibuildwheel==$CIBUILDWHEEL_VERSION
elif [ "$TRAVIS_OS_NAME" = "osx" ]; then
    sudo pip install cibuildwheel==$CIBUILDWHEEL_VERSION
else
    echo Unrecognized OS
    exit -1
fi

cibuildwheel --output-dir dist

# only create the source distribution from linux, so that we don't try to upload it twice
if [ "$TRAVIS_OS_NAME" = "linux" ]; then
    python setup.py sdist --dist-dir dist
fi
