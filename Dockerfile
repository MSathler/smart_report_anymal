FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Copy the Python scripts
COPY codes ./

# Optionally, copy the requirements file and install Python dependencies
#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install watchdog==4.0.0 lxml==5.2.1 pandas==2.2.2 werkzeug==3.0.2 flask==3.0.3 Jinja2==3.1.3 waitress==3.0.0 
# Copy the supervisord configuration file into the container
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run supervisord
CMD ["/usr/bin/supervisord"]
# CMD ["bash"]