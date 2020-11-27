# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#build dependencies needed for pillow to install
RUN apk update \
    && apk add  gcc python3-dev musl-dev\
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.dev.sh .
RUN chmod 777 entrypoint.dev.sh
#copy project
COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.dev.sh"]