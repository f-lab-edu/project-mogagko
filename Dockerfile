# 파이썬 baseimage 선택
From python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN --mount=type=secret,id=ENVIRONMENT \
  --mount=type=secret,id=DB_PASSWORD \
  --mount=type=secret,id=DB_NAME \
  --mount=type=secret,id=DB_HOST \
  --mount=type=secret,id=DB_PORT \
  --mount=type=secret,id=JWT_SECRET \
  --mount=type=secret,id=JWT_ALGORITHM \
  export ENVIRONMENT=$(cat /run/secrets/ENVIRONMENT) && \
  export DB_PASSWORD=$(cat /run/secrets/DB_PASSWORD) && \
  export DB_NAME=$(cat /run/secrets/DB_NAME) && \
  export DB_HOST=$(cat /run/secrets/DB_HOST) && \
    export DB_HOST=$(cat /run/secrets/DB_PORT) && \

  export DB_HOST=$(cat /run/secrets/JWT_SECRET) && \
  export DB_HOST=$(cat /run/secrets/JWT_ALGORITHM)


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
