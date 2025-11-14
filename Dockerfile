FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN python -m venv /opt/venv && . /opt/venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
ENV PATH=/opt/venv/bin:$PATH
CMD ["python", "-m", "pytest", "-q"]
