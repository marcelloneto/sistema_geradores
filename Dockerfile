# Use the official Python image as the base image
FROM python:3.14.3

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the working directory
COPY . /app

# Install the application dependencies
RUN pip install -r requirements.txt

# Informa ao Docker/Servidor a porta padrão do container
EXPOSE 8001

# Inicializa o Django escutando na variável de ambiente PORT (padrão em deploys) ou na 8000
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:${PORT:-8001}"]