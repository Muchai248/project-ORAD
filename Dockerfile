#  use an official python runtime as a parent image
FROM python:3.11.6

# Set environment variables
ENV PYTHONDOWNWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

# set working directory 
WORKDIR /orad

# Install Dependencies
COPY requirements.txt /orad
RUN pip install -r requirements.txt

# copy project to container
COPY . /orad