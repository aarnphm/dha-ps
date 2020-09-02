#!make
.PHONY := help push lint build dev

.DEFAULT_GOAL := dev

BIN := ingress

GO_DIR := $(shell find . -type f -name '*.go' | cut -d "/" -f2 | head -n 1)

LOCAL ?= true

INGRESS_RUN = $(shell cd 'ingress' && go run .)

ifeq ($(LOCAL), true)
	DOC_DIR = docs/ui/dist/swagger.json
else
	DOC_DIR = docs/swagger.json
endif

help: ## List of defined target
	@grep -E '^[a-zA-Z_-]+:.*?##.*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'	

build: ## Go build ingress
	cd $(GO_DIR) && swagger generate spec -o $(DOC_DIR)
ifeq ($(LOCAL), true)
	cd $(GO_DIR)/docs && statik -src ui/dist -p ui -f
endif
	cd $(GO_DIR) && go build -o bin/$(BIN) .

lint: ## Go lint
	cd $(GO_DIR) && golangci-lint run

ingress-dev: ## Run ingress (with reflex to reload when detected changes)
	ulimit -n 1000
	reflex --decoration=fancy -s -r '\.go$$' $(INGRESS_RUN)

pr-dev: ## runs python inference server with FastAPI
	uvicorn price_recommender.main:app --workers 8 --reload --port 5050 --host 0.0.0.0

local: build ## runs dev locally
	$(MAKE) -j 2 pr-dev ingress-dev 

dev: push ## local dev with minikube
## https://unix.stackexchange.com/a/393949/430604
ifeq ($(shell minikube status | sed -n "s/.*host: //p"), "Running")
	minikube start
endif
	kubectl apply -f deploy/minikube.yml

delete: ## remove current deployment
	kubectl delete -n default deployment/ingress
	kubectl delete -n default deployment/pr

docker-%: ## build, run, push with configuration
	docker-compose -f deploy/docker-compose.yml $*

push: build ## build and then push images to registry
	$(MAKE) docker-build && $(MAKE) docker-push
