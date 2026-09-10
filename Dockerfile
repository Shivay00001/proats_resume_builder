FROM python:3.9-slim

# Install Tkinter and X11 dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variable for X11 display
ENV DISPLAY=:0

ENTRYPOINT ["python", "main.py"]
