# RENTAN (Lab L3.3): base image besar, berjalan sebagai root, menyalin seluruh repo,
# dan menjalankan server pengembangan Flask dengan debugger aktif.
FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install -r api/requirements.txt
EXPOSE 5000
CMD ["python", "api/app.py"]
