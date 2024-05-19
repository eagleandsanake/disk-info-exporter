FROM python:3.9-slim
WORKDIR /app
COPY src/collctor.py /app/
COPY src/exportor.py /app/
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python3", "/app/exportor.py"]
