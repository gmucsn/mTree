FROM  continuumio/miniconda3:23.5.2-0
LABEL version="mTree Environment"

RUN apt-get update && apt-get install -y build-essential

ENV APP_HOME /mtree
WORKDIR $APP_HOME
COPY . $APP_HOME

RUN pip install -e /mtree/

# expose port 5000 for flask service
EXPOSE 5000/tcp

SHELL ["/bin/bash"]

ENTRYPOINT ["mTree_developer_server"]
