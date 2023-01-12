FROM python:3.9.6-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Rust Compiler for PyTorch and Detoxify
RUN curl https://sh.rustup.rs -sSf -y | sh

# Create the appropriate directories
ENV APP_HOME=/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
RUN mkdir $APP_HOME/docs
WORKDIR $APP_HOME

RUN apt update
# Install large packages here for faster rebuilds
RUN pip install torch==1.13.1

COPY requirements.txt $APP_HOME
RUN pip install -r requirements.txt

# copy project
COPY . $APP_HOME

ENTRYPOINT [ "sh", "./backend.sh" ]
