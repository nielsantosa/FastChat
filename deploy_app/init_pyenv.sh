## install requirements
sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

## download script and run it
curl https://pyenv.run | bash

# init pyenv
echo '
# init pyenv
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
' >> ~/try.sh

# reset shell
exec $SHELL

# try pyenv
if [ -z $(pyenv --version) ];
then
  echo "pyenv is not installed succesfully";
  exit 0;
else
  echo "pyenv is installed successfully";
fi

# install python 3.11.2
pyenv install 3.11.2

# create virtualenvs for python 3.11.2
pyenv virtualenv 3.11.2 venv-3.11.2

# activate virtualenv 3.11.2
pyenv activate venv-3.11.2
