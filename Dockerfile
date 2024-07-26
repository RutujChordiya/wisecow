# Use an official Node.js runtime as the base image
FROM node:14

# Set the working directory
WORKDIR /usr/src/app

# Install dependencies
RUN apt-get update && apt-get install -y bash fortune-mod cowsay

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 4499

# Command to run the application
CMD ["./wisecow.sh"]
