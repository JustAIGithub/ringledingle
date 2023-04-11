FROM python:3.9

# Update the package list and install necessary dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    ffplay \
    ffprobe

# Set the working directory
WORKDIR /app

# Copy the content of the current directory into the working directory
COPY . /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# gunicorn
# CMD ["gunicorn", "--config", "gunicorn-cfg.py"]
CMD ["python", "run.py"]

