# 1. Use the official lightweight Python image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy just the requirements first (this makes rebuilding faster)
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your project into the container
COPY . .

# 6. Expose the port Flask runs on
EXPOSE 5000

# 7. Tell Docker how to run your app
# We use host 0.0.0.0 so it can be accessed outside the container
ENV FLASK_APP=app/app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]