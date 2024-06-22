
# SoccerIze: Action Detection in Football Videos and Audio Narration Generation

## Project Overview

SoccerIze is a web application designed to detect actions in football videos and generate a narrative audio summary of the events. Leveraging the power of artificial intelligence and deep learning, SoccerIze aims to provide an innovative solution for analyzing football matches, offering real-time spoken narratives to enhance the user experience.

## Features

- **Action Detection**: Identifies key actions in football videos using pre-trained models.
- **Audio Narration**: Generates audio summaries of detected actions, providing an immersive experience.
- **User-Friendly Interface**: Allows users to upload their own videos or select from pre-loaded options for analysis.

## Installation Guide

### Local Installation

To install and run SoccerIze locally, follow these steps:

#### Prerequisites

Ensure your system meets the following requirements:
- Operating System: Windows 10 or higher, Ubuntu 20.04 or higher
- Python: Version 3.11
- GPU: Nvidia GPU capable of handling high computational loads
- CUDA: Version 11.8 installed on the system [CUDA 11.8 Download](https://developer.nvidia.com/cuda-11-8-0-download-archive)

#### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/alblopnov/TFG-codebase
   cd TFG-codebase
   ```

2. **Configure Environment Variables**
   - Copy the `.env.example` file and rename it to `.env`.
   - Run the following command to generate necessary secrets:
     ```bash
     python src/util/secret.py
     ```
   - Update the `.env` file with the generated values and your OpenAI API key. Ensure it looks like the following:
     ```
     SECRET_KEY=example_secret_key
     JWT_SECRET_KEY=example_jwt_secret_key
     ADMIN_USERNAME=user
     ADMIN_PASSWORD=password
     OPENAI_API_KEY=openai_api_key
     ```

3. **Install Pipenv**
   ```bash
   pip install pipenv
   ```

4. **Install Dependencies**
   ```bash
   pipenv install
   ```

5. **Install PyTorch with CUDA Support**
   ```bash
   pipenv run uninstall_torch
   pipenv run install_torch 
   ```

6. **Run the Application**
   ```bash
   pipenv run python src/app.py
   ```
   The application will be available at `http://localhost:5000`.

### Docker Deployment

SoccerIze can also be deployed using Docker. Follow these steps to set up the Docker environment:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/alblopnov/TFG-codebase
   cd TFG-codebase
   ```

2. **Choose the Appropriate Dockerfile**
   - For systems with CUDA support, use the Dockerfile in the `master` branch.
   - If CUDA is not supported, use the Dockerfile in the `aws-despliegue` branch.
     
3. **Update Environment Variables in the Dockerfile**
   - Run the following command to generate necessary secrets:
     ```bash
     python src/util/secret.py
     ```
   - Update the `env` section of the Dockerfile with the generated values and your OpenAI API key. Ensure it looks like the following:
     ```
     SECRET_KEY=example_secret_key
     JWT_SECRET_KEY=example_jwt_secret_key
     ADMIN_USERNAME=user
     ADMIN_PASSWORD=password
     OPENAI_API_KEY=openai_api_key
     ```

3. **Build the Docker Image**
   ```bash
   docker-compose up -d
   ```

## Usage

1. **Access the Application**
   Navigate to the web application URL. Log in using the provided credentials:
   - **Username**: tfg-?admin?
   - **Password**: tfg-?admin?
     
![Login](https://github.com/alblopnov/TFG-codebase/assets/74500641/39182fd3-24c7-4a28-86c4-01a46fd0602e)

2. **Select a Video**
   - You can either upload a new video in `.mp4` format or select from the pre-loaded videos.

![index](https://github.com/alblopnov/TFG-codebase/assets/74500641/86ffaa5a-c9d9-4294-8b64-03db5c64873f)

3. **Upload a Video**
   - Click on "Upload Video" to start the analysis and narration generation. The process may take several minutes depending on the video length.

4. **View Results**
   - Once the processing is complete, the results will be displayed with the video, detected events, and the generated audio narration.

![image](https://github.com/alblopnov/TFG-codebase/assets/74500641/6d4ad938-f7b0-414d-8ae2-971643cde573)

5. **Logout**
   - To log out, click on the logout button. This will clear all session data.

## Pretrained Models

We utilized pretrained models and python scripts from SoccerNet for action detection. These were obtained from [SoccerNet Action Spotting](https://github.com/jhong93/spot).

---
[Demo in Spanish](https://uses0-my.sharepoint.com/:v:/g/personal/alblopnov_alum_us_es/Eb5Rkjln0DFCu78LBa8nPdsBL-eM52VzYIItIIUc3Ve_Zw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=46xHLU)

**Authors**: Alejandro Gallardo Pelayo, Alberto Miguel López-Benjumea Novella  
**Supervisor**: Juan Antonio Álvarez García  
**Institution**: Department of Computer Languages and Systems, Degree in Software Engineering, University of Seville July 2023/24
