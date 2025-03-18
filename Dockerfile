FROM python:3.9-slim
ARG API_KEY
ARG API_KEY_HEADER
ENV API_KEY=${API_KEY}
ENV API_KEY_HEADER=${API_KEY_HEADER}
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY application /app/application
EXPOSE 8000
CMD ["uvicorn", "application.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
