FROM selenium/standalone-chrome:135.0

USER root

# install Python3, pip, venv, Xvfb and cron
RUN apt-get update && apt-get install -y python3-pip python3-venv xvfb build-essential libffi-dev python3-dev cron jq && apt-get clean && rm -rf /var/lib/apt/lists/*

# set Python-related environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# create and activate a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# set up the working directory
WORKDIR /app

# copy the project into /app/ and give ownership to seluser who also runs this script
COPY . /app/
RUN chown -R seluser:seluser /app
# set pythonpath to app
ENV PYTHONPATH=/app
# install dependencies from requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# give execution rights and apply cron job
ADD cronjob /etc/cronjob
RUN chmod 0644 /etc/cronjob
RUN crontab /etc/cronjob

RUN chmod +x /app/bin/empty_collection.py
RUN chmod +x /app/bin/sync_rates.sh
RUN chmod +x /app/src/main.py

# ensure correct permissions for /tmp/.X11-unix to prevent Xvfb from issuing warnings
RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

# Copy the entrypoint script into the container and make it executable
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# run docker-entrypoint shell script
CMD ["/usr/bin/bash", "-c", "/app/docker-entrypoint.sh && tail -f /dev/null"]
