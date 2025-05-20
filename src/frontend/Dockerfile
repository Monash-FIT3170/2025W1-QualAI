FROM node:18

WORKDIR /app

ARG BACKEND_PORT
ENV PORT=$BACKEND_PORT

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE $BACKEND_PORT

CMD ["npm", "run", "dev", "--", "--host"]
