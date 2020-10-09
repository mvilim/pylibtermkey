set -e -x

CIBUILDWHEEL_VERSION_LINUX=1.5.5
CIBUILDWHEEL_VERSION_OSX=1.1.0

if [ "$TRAVIS_OS_NAME" = "linux" ]; then
    pip install cibuildwheel==$CIBUILDWHEEL_VERSION_LINUX
elif [ "$TRAVIS_OS_NAME" = "osx" ]; then
    sudo pip install cibuildwheel==$CIBUILDWHEEL_VERSION_OSX
else
    echo Unrecognized OS
    exit -1
fi

cibuildwheel --output-dir dist

# only create the source distribution from linux, so that we don't try to upload it twice
if [ "$TRAVIS_OS_NAME" = "linux" ]; then
    python setup.py sdist --dist-dir dist
fi
