FROM python:3.11-alpine

WORKDIR /app

# Install bash
RUN apk add --no-cache bash

# Copy all files to the /app directory
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ARG DATABASE_URL
ENV DATABASE_URL=$DATABASE_URL

# Make sure wait-for-it.sh is executable
RUN chmod +x /app/wait-for-it.sh

# Set environment variables
ENV PORT=8000
ENV DATABASE_URL=$DATABASE_URL
ENV JWT_SECRET=$JWT_SECRET
ENV ALGORITHM=$ALGORITHM
ENV ACCESS_TOKEN_EXPIRE_MINUTES=$ACCESS_TOKEN_EXPIRE_MINUTES

EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]