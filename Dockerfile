from hypriot/wiringpi:latest
maintainer chris smith <chris.b.smith@gmail.com>

add ./run.sh /root/
add ./envvals /root/
add ./dockerTemps.py /root/
add ./requirements.txt /root

RUN git clone https://github.com/apixu/apixu-python.git && \
    cd apixu-python && \
    python setup.py install && \
    pip install -r /root/requirements.txt 

ENTRYPOINT bash /root/run.sh
