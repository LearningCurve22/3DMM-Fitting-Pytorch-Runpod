FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Prevent tzdata from prompting
ARG DEBIAN_FRONTEND=noninteractive

# Install system deps (include git BEFORE pip)
RUN apt-get update && apt-get install -y \
    git wget unzip libgl1 cmake ninja-build \
    && rm -rf /var/lib/apt/lists/*

# Copy repo
WORKDIR /workspace
COPY . /workspace

# Install Python deps
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install PyTorch3D (must match PyTorch version)
RUN pip install "git+https://github.com/facebookresearch/pytorch3d.git"

# Runpod handler entrypoint
CMD ["python", "-u", "runpod_handler.py"]
