FROM  continuumio/miniconda3:v25.11.1
LABEL version="MTREE-DEV-CONTAINER-1"

RUN apt-get update && apt-get install -y build-essential

EXPOSE 8000/tcp
# RUN /opt/conda/bin/pip install -e /workspaces/mTree