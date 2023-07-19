ARG VIRTUAL_ENV_NAME=.researchmanagement

# pull image from docker hub (you can also specifiy a remote host to pull from)
FROM python:3.11.3-alpine

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
# install pip package manager
RUN pip install pip --upgrade

RUN adduser -D app
USER app

# set up the current working directory of the container 
WORKDIR /app

# optimization
COPY --chown=app:app requirements.txt .
# install dependecies
RUN pip install --user -r requirements.txt
#RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

ENV PATH=".local/bin:${PATH}"

# copy al files from the current Dockerfile directory to the current WORKDIR inside the container, so all files will be copied into /app/...
COPY --chown=app:app . .

# open container ports
EXPOSE 5001

CMD ["python", "main.py"]
