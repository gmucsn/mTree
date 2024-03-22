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

## Build instructions


# basic build:
# docker build -t mtree/mtree:1.2.1d .
# (M2 mac) docker buildx build --platform=linux/amd64 -t mtree/mtree:1.4.0 .
# (Else) docker build -t mtree/mtree:1.2.1c .


# Pulling:
# docker pull mtree/mtree

# running
# docker run -p 5000:5000 -v /Users/Shared/repos/mTree/mTree_learning_exercises/basic_auctions:/auctions -t -i mtree/mtree:1.0.11e
# docker run -p 5000:5000 -v /Users/Shared/repos/mTree/mTree_learning_exercises/basic_auctions:/auctions -it mtree/mtree:1.0.11e
# docker run -p 5000:5000 -v /Users/Shared/repos/mTree/mTree_learning_exercises/basic_auctions:/auctions -it -d mtree/mtree:1.0.11e bash
# docker run -v /Users/Shared/repos/mTree_auction_examples:/auctions -t -i mtree/mtree:latest

# docker run -p 5000:5000 -v /Users/Shared/repos/mTree/mTree_learning_exercises/basic_auctions:/auctions --network host -it mtree/mtree:1.0.11e
# cd /auctions/sealed_bid_common_value_auction
# mTree_runner -i ./config/basic_simulation.json