FROM amazonlinux

WORKDIR /
RUN yum update -y

# Install Python 3.7
RUN yum install python3 zip -y

# Install pipenv
RUN pip3 install pipenv
RUN pip3 install --upgrade pip


# Install Python packages
RUN mkdir /packages
COPY requirements.txt /packages/requirements.txt
#RUN echo "opencv-python-headless" >> /packages/requirements.txt
#RUN echo "flask" >> /packages/requirements.txt
#RUN echo "numpy" >> /packages/requirements.txt
RUN mkdir -p /packages/picfix-python-3.7/python/lib/python3.7/site-packages
RUN pip3 install -r /packages/requirements.txt -t /packages/picfix-python-3.7/python/lib/python3.7/site-packages

COPY picfix.py


#COPY requirements.txt .
#RUN mkdir -p /packages/picfix-python-3.7/python/lib/python3.7/site-packages
#RUN pip3 install -r requirements.txt -t /packages/picfix-python-3.7/python/lib/python3.7/site-packages

#
#RUN mkdir /packages
#COPY requirements.txt /packages/requirements.txt
#RUN mkdir -p /packages/picfix-python-3.7/python/lib/python3.7/site-packages
#RUN pip3 install -r /packages/requirements.txt -t /packages/picfix-python-3.7/python/lib/python3.7/site-packages

# Create zip files for Lambda Layer deployment
WORKDIR /packages/picfix-python-3.7/
RUN zip -r9 /packages/picfix-python37.zip .
WORKDIR /packages/
RUN rm -rf /packages/picfix-python-3.7/

WORKDIR /
# Command to run on container start
CMD [ "python", "./picfix.py" ]