# 파이썬 baseimage 선택
From python:3.10

# 모든 파일 docker container ./CODE로 COPY
COPY . /CODE

# 현재 workdir를 /CODE로 지정
WORKDIR /CODE

# pipenv 설치 및 라이브러리 설치
RUN pip install pipenv && pipenv install --system

# port 설정
EXPOSE 8000


# fastapi 실행 2
CMD ["/usr/bin/python", "mogako/app/main.py"]
#CMD ["uvicorn", "mogako.app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]