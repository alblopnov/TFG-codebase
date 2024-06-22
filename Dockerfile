FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

WORKDIR /app

# Set non-interactive shell
ENV DEBIAN_FRONTEND=noninteractive \
    SECRET_KEY=b4a3c288889cb271ce427a3d052e2fc75fadc52c1bafeab795e35964671c869c \
    JWT_SECRET_KEY=329c81e4f76128b461d9a8ed32f592e9a92a725c92df1125f753e5be77cc398b \
    ADMIN_USERNAME=tfg-?admin?\
    ADMIN_PASSWORD=tfg-?admin?\
    OPENAI_API_KEY=api_key \
    PYTHONPATH=/app 

# Install dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.11 python3.11-venv python3-pip python3-dev ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . /app

# Install pipenv
RUN pip install pipenv

# Install Python dependencies
RUN pipenv --python 3.11 install

# Install PyTorch with CUDA support
RUN pipenv run pip3 uninstall -y torch torchvision torchaudio
RUN pipenv run pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Expose port for the application
EXPOSE 5000

# Command to run the application
CMD ["pipenv", "run", "python3", "/app/src/app.py"]