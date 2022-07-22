FROM  continuumio/miniconda3:4.10.3
LABEL Author, S. Kunath
LABEL version="1.1"

RUN apt-get update && apt-get install -y procps vim
ENV APP_HOME /mtree
WORKDIR $APP_HOME
COPY . $APP_HOME
#COPY ../mTree $APP_HOME/mTree

#---------------- Prepare the envirennment
RUN conda update --name base conda 
RUN python /mtree/setup.py develop

# need to fix to use correct profile as well...
# switch here makes startup of the CLI from docker decsktop easier
RUN mv /bin/sh /bin/osh && ln -s /bin/bash /bin/sh

# expose port 5000 for flask service
EXPOSE 5000/tcp

SHELL ["/bin/bash"]
WORKDIR /auctions
ENTRYPOINT ["mTree_developer_server"]

# basic build:
# docker build -t mtree/mtree:1.1.4 .

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