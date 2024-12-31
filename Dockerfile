FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "--reload", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]