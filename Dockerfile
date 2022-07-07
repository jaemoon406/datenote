FROM python:3.9.0
WORKDIR /server
RUN apt-get update
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN git clone https://github.com/jaemoon406/datenote.git .
RUN echo "clone Success"
#COPY requirements.txt /server/
RUN python3 -m venv venv
RUN  . /server/venv/bin/activate
RUN pip install -r requirements.txt
RUN echo "Finish"
CMD ["python manage.py runserver \
    --settings=datebook.settings.local && gunicorn datebook.wsgi \
    --bind 0.0.0.0:8000"]