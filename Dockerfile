# UPDATED ON 4-29-23 
FROM python:3.9

# Install necessary packages
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends ffmpeg curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js and npm
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

# Set the working directory
WORKDIR /app

# Copy the content of the current directory into the working directory
COPY . /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install Tailwind CSS, postcss, and autoprefixer as development dependencies
RUN npm install tailwindcss@latest postcss@latest autoprefixer@latest --save-dev

# Create a configuration file for Tailwind CSS and PostCSS
RUN npx tailwindcss init -p

# CMD ["gunicorn", "--config", "gunicorn-cfg.py"]
CMD ["python", "run.py"]
