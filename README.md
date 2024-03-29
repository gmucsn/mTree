# mTree

Documentation can be found [here](http://mtree.readthedocs.io/en/latest/).

mTree can be installed using the `pip` installer.

```
pip3 install mTree
```

Once installed, mTree is imported in the standard fashion.

```python
import mTree
```

# Development

Running the set up:

Go to the directory and enter the following:

```commandline
python setup.py develop
```

If you are using macOS:
```commandline
python3.6 setup.py bdist_egg
```

For Windows:
```commandline
python setup.py bdist_egg
```

After building this you will need to install locally:

```commandline
easy_install dist/mTree-x-py3.6.egg
```


To test this, open python3 in either Terminal or Command Prompt, and try importing mTree with:

```python
import mTree
```

If there are no error messages, the build was successful.
You can now access mTree as you would any other python package.


Thespian Logging notes:

THESPLOG_FILE
THESPLOG_FILE_MAXSIZE
export THESPLOG_FILE="/tmp/thespian.log"
export THESPLOG_THRESHOLD="DEBUG"

export THESPLOG_FILE="./thespian.log"
export THESPLOG_THRESHOLD="DEBUG"

Checking for python processes in powershell:
 ps *python* 

kill all python processes in powershell:
Stop-Process -Name "python" -Force

Docker dom