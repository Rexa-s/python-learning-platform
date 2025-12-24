FROM python:3.11-slim

# Render uses /opt/render/project/src
WORKDIR /opt/render/project/src

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 5001

# Run the app directly
CMD ["python", "-m", "flask", "--app", "backend.app", "run", "--host", "0.0.0.0", "--port", "5001"]
