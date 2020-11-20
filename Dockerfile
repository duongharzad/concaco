FROM python:3.7.3-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code/
WORKDIR /code/
RUN apk add --update --no-cache \
        python3-dev \
        libstdc++ \
        # Pillow dependencies
        jpeg-dev \
        zlib-dev \
        freetype-dev \
        lcms2-dev \
        openjpeg-dev \
        tiff-dev \
        tk-dev \
        tcl-dev \
        harfbuzz-dev \
        g++ \
        mariadb-dev \
        # mariadb-client \
        fribidi-dev \
        curl

RUN apk update && apk add --no-cache \
        msttcorefonts-installer \
        fontconfig \
        libx11 \
        libxml2 \
        libxml2-dev \
        libxslt-dev \
        libxrender \
        libxext \
        ca-certificates \
        && curl https://mirrors.xtom.com/osdn//sawarabi-fonts/66581/sawarabi-gothic-20161015.zip > sawarabi-gothic-20161015.zip \
        && unzip sawarabi-gothic-20161015.zip -d /usr/share/fonts/truetype/ \
        && update-ms-fonts \
        && fc-cache -f \

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev wkhtmltopdf

ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /code/

EXPOSE 80
CMD exec uwsgi --http :80 --module web.wsgi