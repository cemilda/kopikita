# RENTAN (Lab L3.3): base image besar, berjalan sebagai root, menyalin seluruh repo,
# dan menjalankan server pengembangan Flask.
FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install -r api/requirements.txt
EXPOSE 5000
# app.py kini hanya mendengar di 127.0.0.1 (L2.3), jadi container perlu host sendiri.
CMD ["sh", "-c", "python api/db.py && cd api && exec flask --app app run --host 0.0.0.0 --port 5000"]
