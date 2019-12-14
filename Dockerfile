from ubuntu:18.10

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip nginx
RUN pip3 install uwsgi

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["./run.sh"]
#CMD ["tail -f /dev/null"]
#ENTRYPOINT ["python3"]
#CMD ["start_app.py"]
#ENTRYPOINT ["sh"]
