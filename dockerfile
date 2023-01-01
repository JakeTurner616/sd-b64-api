FROM python:3.8-slim

# Create a directory for the app
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the app code
COPY web.py .
COPY sd.py .
COPY prompt.txt .
COPY static static/
COPY templates templates/

# Expose the default port for the Flask app
EXPOSE 5000

# Set the default command to run the Flask app "timeout" is important to let the API respond before the process is killed.
CMD ["gunicorn", "web:app", "-b", "0.0.0.0:5000", "--timeout", "100"]
