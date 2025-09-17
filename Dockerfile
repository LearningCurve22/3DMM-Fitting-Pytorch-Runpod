# Base image: PyTorch with CUDA 12.8 and cuDNN
# If RunPod provides its own base image, you can replace this with that.
FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel


# Set working dir
WORKDIR /app

# copy repo
COPY . /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    wget \
    unzip \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Python deps - install most libs via pip
# Note: we avoid installing torch here if the base image already contains a working torch
# If your base DOES NOT have torch, uncomment the pip install torch line and set the right index-url for your CUDA.
RUN pip install --upgrade pip

# Install GPU-enabled PyTorch only if needed.
# Uncomment and adapt the following if your base image doesn't already have torch:
# RUN pip install --index-url https://download.pytorch.org/whl/cu128 \
#     "torch" "torchvision" "torchaudio"

# Install pytorch3d (recommended to install from official instructions for matching torch)
# Keep this as the pip install; if it fails, match the version to torch installed in the image.
RUN pip install 'git+https://github.com/facebookresearch/pytorch3d.git'

# Install the rest of the python requirements in one go
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Expose API port
EXPOSE 8000

# Create results dir
RUN mkdir -p /app/results /app/BFM /app/uploads

# Entrypoint for the RunPod handler (this will be the API app)
#CMD ["uvicorn", "runpod_handler:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# Entrypoint for RunPod serverless
CMD ["python", "-u", "runpod_handler.py"]
