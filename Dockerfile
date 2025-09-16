FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

ARG DEBIAN_FRONTEND=noninteractive

# Install system deps (must include git before pip install)
RUN apt-get update && apt-get install -y \
    git wget unzip libgl1 cmake ninja-build \
    build-essential python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY . /workspace

# Upgrade pip, setuptools, wheel
RUN pip install --upgrade pip setuptools wheel

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt --verbose \
    --extra-index-url https://download.pytorch.org/whl/cu118

# Install PyTorch3D (match torch 2.1.0 + CUDA 11.8 + Python 3.10)
RUN pip install --no-cache-dir pytorch3d \
    -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu118_pyt210/download.html


CMD ["python", "-u", "runpod_handler.py"]
