FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src ./src
COPY ./tests ./tests
RUN pytest .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]