FROM ubuntu:22.04

# Install basic tools
RUN apt-get update && apt-get install -y \
    curl wget git build-essential \
    software-properties-common \
    lsb-release

# Install Python
RUN apt-get install -y python3 python3-pip python3-venv
RUN pip3 install --upgrade pip
RUN pip3 install black isort pylint pytest

# Install Go
RUN wget https://go.dev/dl/go1.23.1.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.23.1.linux-amd64.tar.gz && \
    rm go1.23.1.linux-amd64.tar.gz
ENV PATH=$PATH:/usr/local/go/bin

RUN go install golang.org/x/tools/cmd/goimports@latest

# Install C++ (GCC + Clang)
RUN apt-get install -y g++ clang clang-format gdb valgrind

# Install Java
RUN apt-get install -y openjdk-17-jdk maven

# Set working directory
WORKDIR /workspace