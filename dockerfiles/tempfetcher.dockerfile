FROM python:3.8

WORKDIR /usr/src/app

COPY src/requirements/tempfetcher_req.txt ./
RUN pip install --no-cache-dir -r tempfetcher_req.txt

COPY src/tempfetcher.py .

CMD [ "python","-u" ,"./tempfetcher.py" ]