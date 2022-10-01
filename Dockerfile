# 파이썬 baseimage 선택
From python:3.10

# 환경변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 모든 파일 docker container ./app로 COPY
COPY . /app

# 현재 workdir를 /app로 지정
WORKDIR /app

ENV PYTHONPATH /app

# pipenv 설치 및 라이브러리 설치
RUN pip install pipenv && pipenv install --system

# port 설정
EXPOSE 8000


# main.py 실행
CMD ["/bin/sh", "-c" , "alembic upgrade head && /usr/local/bin/python mogako/app/main.py"]
