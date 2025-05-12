# Use a Python base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy backend app into the container
COPY ./app /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI app's port (adjust if different)
EXPOSE 5000

# Command to run the Flask app
# CMD ["python", "app.py"]

CMD ["flask", "run","--host=0.0.0.0"]

