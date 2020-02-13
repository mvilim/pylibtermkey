set -e -x

if [ "$(uname)" == "Linux" ]; then
    yum install -y ncurses-devel
elif [ "$(uname)" == "Darwin" ]; then
    # no osx specific operations
    :
else
    echo Unrecognized OS
    exit -1
fi

pip install cmake
