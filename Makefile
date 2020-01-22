NAME = tick
VERSION = 1.0.0
IMAGE = reg.lab.st/$(NAME):$(VERSION)

build:
	docker build -t $(IMAGE) .

push: build
	docker push $(IMAGE)

.PHONY: build push