FROM python:3.8

WORKDIR /usr/src/app

COPY src/requirements/dash_app_req.txt ./
RUN pip install --no-cache-dir -r dash_app_req.txt

COPY src/app.py .

EXPOSE 3000

#CMD [ "python","-u" ,"./app.py" ]

CMD [ "gunicorn", "--workers=2", "--threads=4", "-b 0.0.0.0:8000", "app:server"]
