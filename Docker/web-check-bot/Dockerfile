FROM ubuntu:latest


RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get -y install python3-pip


RUN useradd -d /home/web-check-bot/ -m -p bot_runner -s /bin/bash bot_runner
RUN echo "bot_runner:bot_runner" | chpasswd

WORKDIR /home/bot_runner
COPY * .
RUN pip3 install -r requirements.txt
RUN chown -R root:root /home/bot_runner

CMD [ "python3", "./main.py"]
