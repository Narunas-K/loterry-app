# #Specify base image
# FROM node:alpine
#
# #Install some dependencies
# WORKDIR /usr/app
# COPY ./package.json ./
# RUN npm install
# RUN npm install body-parser --save
# COPY ./ ./
# #Default command
# CMD ["npm", "start"]

FROM node
WORKDIR /usr/app
COPY ./package.json ./
RUN apt-get update
# RUN pip install redis
RUN apt-get install -y libzmq3-dev
RUN apt-get install -y libevent-dev
# RUN pip install pyzmq
# RUN pip install zerorpc
RUN npm install
RUN npm install body-parser --save
RUN npm install -g --unsafe-perm zerorpc
RUN npm install redis
RUN npm install ioredis
RUN npm install express-validator
RUN npm install popups
RUN npm install ejs
COPY ./ ./
CMD ["npm", "start"]