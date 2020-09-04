#!make
.PHONY := all

all: help dev lint build

.DEFAULT_GOAL := dev

BIN := ingress

GO_DIR := $(shell find . -type f -name '*.go' | cut -d "/" -f2 | head -n 1)

LOCAL ?= true

INGRESS_RUN = $(shell cd 'ingress' && go run .)


help: ## List of defined target
	@grep -E '^[a-zA-Z_-]+:.*?##.*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'	

build: ## Go build ingress
	cd $(GO_DIR) && swagger generate spec -o docs/swagger.yml
	cd $(GO_DIR) && statik -src=docs -f -p docs 
	cd $(GO_DIR) && go build -o bin/$(BIN) .

lint: ## Go lint
	cd $(GO_DIR) && go test ./...
	cd $(GO_DIR) && golangci-lint run

ingress-dev: ## Run ingress (with reflex to reload when detected changes)
	ulimit -n 1000
	reflex --decoration=fancy -s -r '\.go$$' $(INGRESS_RUN)

pr-dev: ## runs python inference server with FastAPI
	uvicorn price_recommender.main:app --workers 8 --reload --port 5000 --host 0.0.0.0

local-dev: build ## runs dev locally
	$(MAKE) -j 2 pr-dev ingress-dev 

dev: push ## local dev with minikube
	$(MAKE) delete
	kubectl apply -f deploy/minikube.yml

delete: ## remove current deployment
	kubectl delete -n default deployment --all

docker-%: ## build, run, push with configuration
	docker-compose -f deploy/docker-compose.yml $*

push: build ## build and then push images to registry
	$(MAKE) docker-build && $(MAKE) docker-push
