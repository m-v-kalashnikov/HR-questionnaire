FROM node:14.3.0-alpine

# make the 'app' folder the current working directory
WORKDIR /app

RUN npm install yarn

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
RUN yarn install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

EXPOSE 8080

CMD ["yarn", "run", "dev"]
