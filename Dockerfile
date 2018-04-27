FROM ubuntu:latest
MAINTAINER Michael Vershinin, goldver@gmail.com

# Params
ENV ENV_PROFILE xyz
ENV VERSION NO-VERSION
ENV SCRIPT bash

# Installing libraries..
RUN apt-get update -q
RUN DEBIAN_FRONTEND=noninteractive apt-get --yes -q install postgresql-client-9.5 redis-tools vim zip htop ctop python-pip python3-pip groff-base curl
RUN pip install awscli
RUN pip3 install requests
RUN curl -fL https://getcli.jfrog.io | sh
RUN mv /jfrog /bin/

# Creating folders..
RUN mkdir -p /root/.jfrog/ /deploy/ mkdir -p /root/.aws/

# Copying configurations..
COPY config/jfrog-cli.conf /root/.jfrog/
COPY config/aws-config /root/.aws/config
COPY config/aws-credentials /root/.aws/credentials
COPY config/root-profile /root/.profile

# Copying scripts and their resources..
COPY scripts/* /md_deploy/

# Run job..
WORKDIR /md_deploy
RUN chmod +x /md_deploy/run.sh

CMD [ "/md_deploy/run.sh" ]
ENTRYPOINT [ "sh", "-c" ]
