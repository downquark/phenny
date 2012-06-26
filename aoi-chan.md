```bash
sudo apt-get -y install python3 python3-minimal python3-mock python3-nose python3-pkg-resources python3-tk python3.2 python3.2-minimal libpython3.2 python3-dev python3-lxml python3.2-dev python-virtualenv libxml2-dev libxslt1-dev idle-python3.2 idle3 git-core
easy_install pip nose lxml
pip install virtualenv virtualenvwrapper feedparser mock cython
```

You will want to add these command to your shell startup file:
`echo WORKON_HOME=~/.virtualenvs` - home for virtual environments
`source /usr/local/bin/virtualenvwrapper.sh`
Change the path to virtualenvwrapper.sh depending on where it was installed by pip.

```bash
git clone git@github.com:downquark/phenny.git ~/code/phenny/
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='-p /usr/bin/python3'
mkvirtualenv phenny -a ~/code/phenny/

cd $WORKON_HOME/phenny/build/
wget https://launchpad.net/oursql/py3k/py3k-0.9.3/+download/oursql-0.9.3.zip
unzip oursql-0.9.3.zip
mv oursql-0.9.3 oursql
cd oursql/
python setup.py build_ext
python setup.py install

workon phenny
```
1. Run `./phenny` - this creates a default config file
2. Edit `~/.phenny/default.py`
3. Run `./phenny` - this now runs phenny with your settings
