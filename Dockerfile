FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

RUN apt-get update && apt-get install -y git wget unzip libgl1 cmake ninja-build

WORKDIR /workspace
COPY . /workspace

# Upgrade pip tools
RUN echo "=== Upgrading pip/setuptools/wheel ===" && \
    pip install --upgrade pip setuptools wheel

RUN echo "=== Installing Python requirements.txt ===" && \
    pip install -r requirements.txt

# Install PyTorch3D (must match PyTorch version)
# RUN pip install "git+https://github.com/facebookresearch/pytorch3d.git"

CMD ["python", "-u", "runpod_handler.py"]
