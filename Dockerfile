# 1. Start with a tiny version of Linux that already has Python
FROM python:3.11-slim

# 2. Create a folder inside that tiny Linux called /app
WORKDIR /app

# 3. Copy your requirements file into that folder
COPY requirements.txt .

# 4. Tell that tiny Linux to install Flask
RUN pip install -r requirements.txt

# 5. Copy your app.py into the folder
COPY . .

# 6. Tell the container to open Port 5000 (the door to your app)
EXPOSE 5000

# 7. The final command: Start the app
CMD ["python", "app.py"]