default: build run

build:
	docker build -t udacity .

run:
	docker run --rm -v $(shell pwd):/home/jovyan/work -p 8888:8888 udacity
