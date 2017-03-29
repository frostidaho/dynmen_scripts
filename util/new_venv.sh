#!/usr/bin/bash
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
DIR="$(dirname $DIR)"
VENVPATH="$DIR/.venv"

virtualenv --system-site-packages "$VENVPATH"
source "$VENVPATH/bin/activate"
# echo $(which python)
# echo $(which pip)
pip install -e "$DIR"
pip install --ignore-installed ipython
pip install --ignore-installed jedi
deactivate

