FROM python:3.9.1-slim-buster
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip install -r requirements.txt
EXPOSE 80
ENV NAME World
CMD ["python", "Painter.py"]