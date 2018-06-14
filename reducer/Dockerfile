FROM python:3
COPY . /tmp
ENV MQ_HOST='rabbit'
ENV REDIS_HOST='192.168.199.160'
RUN cd /tmp &&\
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt
WORKDIR /tmp
ENTRYPOINT python3 main.py