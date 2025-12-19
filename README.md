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

## Developer Documentation

mTree makes use of pdoc to document the code inside this repository. Assuming you have mTree installed you should be able to type `pdoc mTree` and the pdoc webserver will start and be available at http://localhost:8080


## Version 2 adaptive markets

This will have a submodule reference to the adaptive 
`git submodule init`

You will access this repository inside the mTree_adaptive_markets folder inside of this.

These repositories will have to be somewhat manually synchronized.


# Extra Commands


ps aux  |  grep -i Actor  |  awk '{print $2}'  |  xargs sudo kill -9

# Logging Information

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


docker buildx build --platform=linux/amd64 -t mtree/mtree:2.0.0-pre2 .


docker buildx build --platform=linux/amd64 -t mtree/mtree:2.0.1e .

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