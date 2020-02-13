set -e -x

if [ "$TRAVIS_OS_NAME" = "linux" ]; then
    yum install -y ncurses-devel
elif [ "$TRAVIS_OS_NAME" = "osx" ]; then
    # no osx specific operations
    :
else
    echo Unrecognized OS
    exit -1
fi

pip install cmake
