FROM python:3.9

# Install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg ffprobe && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the content of the current directory into the working directory
COPY . /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# gunicorn
# CMD ["gunicorn", "--config", "gunicorn-cfg.py"]
CMD ["python", "run.py"]
