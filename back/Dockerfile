FROM python:3.9.2-alpine

# Upgrade pip
RUN pip install --upgrade pip

# Get curl for healthchecks
RUN apk add --no-cache curl

# Install Jinja2 for templating
RUN pip install Jinja2

# Permissions and non-root user for tightened security
RUN adduser -D nonroot
RUN mkdir /home/app/ && chown -R nonroot:nonroot /home/app
RUN mkdir -p /var/log/fastapi-app && touch /var/log/fastapi-app/fastapi-app.err.log && touch /var/log/fastapi-app/fastapi-app.out.log
RUN chown -R nonroot:nonroot /var/log/fastapi-app
WORKDIR /home/app
USER nonroot

# Copy all the files to the container
COPY --chown=nonroot:nonroot . .

# Create a virtual environment
ENV VIRTUAL_ENV=/home/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Define the port number the container should expose
EXPOSE 5000

# Start uvicorn 
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
