FROM python:3.7

RUN apt-get update -y && \
  apt-get install build-essential -y && \
  pip install --upgrade pip

WORKDIR /tmp
RUN wget http://download.osgeo.org/libspatialindex/spatialindex-src-1.7.1.tar.gz && \
  tar -xvzf spatialindex-src-1.7.1.tar.gz && \
  cd spatialindex-src-1.7.1 && \
  ./configure && \
  make && \
  make install && \
  cd - && \
  rm -rf spatialindex-src-1.7.1* && \
  ldconfig

RUN pip install geopandas==0.6.1 pyproj==2.4.0 Pyrebase==3.0.27 \
    Flask==1.1.1 python-dotenv==0.12.0 numpy==1.18.1 matplotlib==3.1.3 \
    mplleaflet==0.0.5 Rtree==0.9.3 pyfcm==1.4.7 geocoder==1.38.1 \
    pandas==0.23.4 urllib3==1.25.8 gunicorn==20.0.4

WORKDIR /Geospatial

COPY Geospatial/ .

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]
