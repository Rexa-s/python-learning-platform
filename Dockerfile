FROM python:3.11-slim

# Render uses /opt/render/project/src
WORKDIR /opt/render/project/src

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Set Flask app
ENV FLASK_APP=backend/app.py
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5001

# Run with Waitress
CMD ["python", "-c", "from waitress import serve; from backend.app import app; serve(app, host='0.0.0.0', port=5001)"]
