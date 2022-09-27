# 파이썬 baseimage 선택
From python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN echo $JWT_SECRET
RUN echo $ENVIRONMENT
RUN echo $DB_PORT


ENV ENVIRONMENT=$ENVIRONMENT
ENV DB_PORT=$DB_PORT
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_USER=$DB_USER
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_NAME=$DB_NAME
ENV DB_HOST=$DB_HOST
ENV JWT_SECRET=$JWT_SECRET
ENV JWT_ALGORITHM=$JWT_ALGORITHM

RUN echo $JWT_SECRET
RUN echo $ENVIRONMENT
RUN echo $DB_PORT



# 모든 파일 docker container ./app로 COPY
COPY . /app

# 현재 workdir를 /app로 지정
WORKDIR /app

ENV PYTHONPATH /app





# pipenv 설치 및 라이브러리 설치
RUN pip install pipenv && pipenv install --system

# port 설정
EXPOSE 8000

# fastapi 실행
CMD ["/usr/local/bin/python", "mogako/app/main.py"]
