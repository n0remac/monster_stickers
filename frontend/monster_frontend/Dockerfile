# The base image
FROM node:alpine

# Set the working directory
WORKDIR /frontend/monster_frontend

# Add the package.json and package-lock.json to install dependencies
COPY package.json package-lock.json ./

# Install the dependencies
RUN npm install

# Copy the main application
COPY . ./

# Set the build command to run when this image is created
RUN npm run build

# Set the command to start the container
CMD ["npm", "start"]