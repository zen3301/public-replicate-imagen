FROM nvidia/cuda:11.8.0-base-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and tools for adding NVIDIA's repository
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    wget \
    gnupg \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

# Add NVIDIA's package repository for cuDNN (modern approach, non-interactive)
RUN wget -O cuda-keyring.asc https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub \
    && cat cuda-keyring.asc | gpg --dearmor --yes -o /usr/share/keyrings/cuda-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/cuda-archive-keyring.gpg] https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64 /" > /etc/apt/sources.list.d/cuda.list \
    && rm cuda-keyring.asc

# Install cuDNN 8 (let Replicate handle the download)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcudnn8 \
    && rm -rf /var/lib/apt/lists/*

# Install cog for local validation
RUN pip install cog

WORKDIR /src
COPY . /src