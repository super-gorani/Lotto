FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "lotto_project.wsgi:application", "--bind", "0.0.0.0:8000"]
