FROM python:3.10

WORKDIR /app

COPY . /app

# Install system dependencies (uncomment if needed)
# RUN apt-get update && apt-get install -y build-essential gcc libffi-dev libssl-dev default-libmysqlclient-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirement.txt

# ENV PYTHONUNBUFFERED=1

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]