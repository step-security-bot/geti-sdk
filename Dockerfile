FROM python:3.8@sha256:77e340f69aafc51cd88769eb690e4ac8bcbd20a29dc540d403a5c4d3fd78198f

RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python

WORKDIR /app

COPY requirements/requirements.txt requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
RUN pip install .

CMD /bin/bash
