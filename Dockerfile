FROM python:3.9-slim-bullseye
WORKDIR /blockchain
# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
# COPY . .
EXPOSE 5000 5001 5002
# CMD . /opt/venv/bin/activate && exec python main.py && exec python node1.py && exec python node2.py
