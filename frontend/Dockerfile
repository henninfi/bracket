# Step 1: Use an official Node.js runtime as a parent image
FROM node:latest

# Step 2: Set the working directory in the container
WORKDIR /usr/src/app

# Step 3: Copy the package.json and package-lock.json (or yarn.lock)
# to leverage Docker cache layering
COPY package*.json ./

# Step 4: Install your application's dependencies
RUN npm install --legacy-peer-deps

# Step 5: Copy the rest of your application's source code
COPY . .

# Step 6: Run npm update
RUN npm update --legacy-peer-deps

# Step 7: Build your Next.js application
# This step compiles your application and gets it ready for deployment
RUN NEXT_PUBLIC_API_BASE_URL="https://bracket-api.rankit.no" npm run build

# Step 8: Your app binds to port 3000 so you'll use the EXPOSE instruction
# to have it mapped by the docker daemon. Adjust if your app uses a different port
EXPOSE 3000

# Step 9: Define the command to run your app using CMD
CMD ["npm", "run", "start"]
