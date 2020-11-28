# pull official base image
FROM amd64/python:3.7.9

# set work directory
WORKDIR /usr/src/

#copy the entrypoint script
COPY entrypoint.sh .
RUN chmod 777 entrypoint.sh

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN apt-get update 
RUN apt-get install -y gcc python3-dev \
         gfortran liblapack3 liblapack-dev libblas-dev

#copy project code in and install python requirements
RUN mkdir app
WORKDIR /usr/src/app
COPY ./textgeneration .
COPY requirements.txt requirements.txt
#RUN pip install django
RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/src/entrypoint.sh"]