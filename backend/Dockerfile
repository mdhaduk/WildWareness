# Use official Python image
FROM python:3.12

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port 5000 to allow external access
EXPOSE 5000

# Set Flask environment variables
ENV FLASK_APP=api.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production
ENV DB_USERNAME="wildfire"
ENV DB_PASSWORD="Appleid123!"



# Run Flask in production mode
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "api:app"]
