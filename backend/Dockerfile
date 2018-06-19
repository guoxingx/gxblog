FROM python:3

COPY ./ /backend
WORKDIR /backend
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
RUN python -m solc.install v0.4.21
ENV PATH="/root/.py-solc/solc-v0.4.21/bin:${PATH}"

# FROM tiangolo/uwsgi-nginx:python3.6
# 
# RUN pip install flask
# 
# ENV NGINX_MAX_UPLOAD 1m
# ENV UWSGI_INI /app/uwsgi.ini
# # ENV STATIC_URL /static
# ENV STATIC_PATH /app/app/static/
# 
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh
# 
# COPY ./ /app
# WORKDIR /app
# RUN pip install -r requirements.txt
