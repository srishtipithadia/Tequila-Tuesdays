# Set base image (host OS)
FROM python:3.9.6

# Set the working directory in the container
WORKDIR /var/site

# Copy the dependencies file to the working directory
COPY requirements.txt .
ENV STATIC_URL /static
ENV STATIC_PATH ./static
ENV FLASK_APP=app.py

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . . 

# By default, listen on port 5000
EXPOSE 80/tcp

# Specify the command to run on container start
#CMD [ "python3", "./app.py" ]
CMD ["flask", "run", "--host=0.0.0.0","--port=80"]
#CMD ["bash"]
