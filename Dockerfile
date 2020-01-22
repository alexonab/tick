FROM python:3.8

ENV TA_TAR ta-lib-0.4.0-src.tar.gz

RUN \
  wget --quiet http://prdownloads.sourceforge.net/ta-lib/${TA_TAR} \
  && tar -C /opt -xzf ${TA_TAR} && rm ${TA_TAR} \
  && cd /opt/ta-lib && ./configure --prefix=/usr && make && make install \
  && pip install pipenv

COPY Pipfile* /
RUN pipenv install

COPY *.py /

ENTRYPOINT ["pipenv", "run"]