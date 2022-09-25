FROM python:3.9-slim


#WORKDIR /src/

# RUN pip3 install --upgrade pip

RUN pip3 install pymodbus && \
    pip3 install numpy

COPY device.py .
COPY config.json .



CMD [ "python3", "./device.py" ]

