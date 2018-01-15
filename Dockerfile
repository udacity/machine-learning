FROM python:3.6.3

WORKDIR /machine-learning
COPY . .

RUN pip install pipenv==9.2.7
RUN pipenv install --system --dev --deploy
