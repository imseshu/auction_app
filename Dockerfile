FROM alpine:latest

WORKDIR /app

RUN apk add --no-cache python3 py3-pip

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 6924

ENTRYPOINT [ "python3", "app.py" ]