FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
CMD ["python", "-m", "unittest", "discover", "-v"]
