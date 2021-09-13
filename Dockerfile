FROM  continuumio/miniconda3:4.9.2
LABEL Author, S. Kunath
LABEL version="0.9"

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
# docker build -t mtree/mtree:1.0.9 .

# Pulling:
# docker pull mtree/mtree

# running
# docker run -v /Users/Shared/repos/mTree_auction_examples:/auctions -t -i mtree/mtree:latest
# cd /auctions/sealed_bid_common_value_auction
# mTree_runner -i ./config/basic_simulation.json