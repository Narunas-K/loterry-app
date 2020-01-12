FROM node
WORKDIR /usr/app
COPY ./package.json ./
RUN apt-get update
RUN apt-get install -y libzmq3-dev
RUN apt-get install -y libevent-dev
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