FROM ubuntu:24.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y vim
RUN apt install -y python3.12 python3-pip python3-venv
WORKDIR /task_manager_server
SHELL ["/bin/bash", "-c"]
# handle python dependencies
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt .
RUN source $VIRTUAL_ENV/bin/activate && pip3 install -r requirements.txt
# prepare server enviroment
COPY . .
CMD python3 manage.py migrate
ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]