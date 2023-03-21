FROM amazonlinux:latest

# Install basic tools needed
RUN yum install -y python3-pip npm make unzip

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install

# Install poetry
RUN pip3 install -U poetry
