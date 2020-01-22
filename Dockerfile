FROM python:3.8-alpine

ENV TA_TAR ta-lib-0.4.0-src.tar.gz

RUN \
  apk add --no-cache --update alpine-sdk \
  && wget --quiet http://prdownloads.sourceforge.net/ta-lib/${TA_TAR} \
  && tar -C /opt -xzf ${TA_TAR} && rm ${TA_TAR} \
  && cd /opt/ta-lib && ./configure --prefix=/usr && make && make install && cd - \
  && pip install pipenv

COPY Pipfile* /
RUN pipenv install

COPY *.py /

CMD ["pipenv", "run", "/impulse.py"]