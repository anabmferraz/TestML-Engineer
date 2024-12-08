FROM python:3.12-bookworm

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Set environment variable for Flask
ENV APP_HOME /back-end
ENV PORT 8080

WORKDIR $APP_HOME

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy rest of the application
COPY . .

# Create and set permissions for database file
RUN touch database.json && chmod 666 database.json

# Expose the port
EXPOSE $PORT

# Run the web service on container startup
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app