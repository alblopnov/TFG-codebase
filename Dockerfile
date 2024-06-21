FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    SECRET_KEY=b4a3c288889cb271ce427a3d052e2fc75fadc52c1bafeab795e35964671c869c \
    JWT_SECRET_KEY=329c81e4f76128b461d9a8ed32f592e9a92a725c92df1125f753e5be77cc398b \
    ADMIN_USERNAME=tfg-?admin?\
    ADMIN_PASSWORD=tfg-?admin?\
    OPENAI_API_KEY=api_key \
    PYTHONPATH=/app 

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip3 install pipenv

# Copy Pipfile and Pipfile.lock first to leverage Docker cache
COPY Pipfile Pipfile.lock /app/

# Install project dependencies
RUN pipenv install

# Uninstall torch packages and install CPU versions
RUN pipenv run pip uninstall -y torch torchvision torchaudio
RUN pipenv run pip install torch torchvision torchaudio

# Copy application code
COPY . /app

# Expose port for the application
EXPOSE 5000

# Command to run the application
CMD ["pipenv", "run", "python", "src/app.py"]