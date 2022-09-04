# 파이썬 baseimage 선택
From python:3.10

# git clone
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT dev

RUN mkdir CODE

COPY . /CODE

WORKDIR /CODE


RUN pip install pipenv && pipenv install --system

# port 설정
EXPOSE 8000


# fastapi 실행
# ENTRYPOINT ["python", "mogako/app/main.py"]
CMD ["uvicorn", "mogako.app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
