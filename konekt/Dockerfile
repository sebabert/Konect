FROM python:3.9-slim-buster

RUN mkdir /code
WORKDIR /code
ADD . /code
RUN apt update && \
    apt -y upgrade && \
    mkdir /usr/share/man/man1/ && \
    apt install openjdk-11-jdk poppler-utils tesseract-ocr tesseract-ocr-fra default-libmysqlclient-dev libpq-dev gcc -y &&  \
    python -m pip install --upgrade pip &&  \
    pip install -r requirements.txt --use-deprecated=legacy-resolver &&  \
    python -m spacy download fr_core_news_sm &&  \
    apt -y clean all
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="/opt/java/openjdk/bin:$PATH"

EXPOSE 8000
CMD ["python", "/code/manage.py", "makemigrations"]
CMD ["python", "/code/manage.py", "migrate"]
CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
