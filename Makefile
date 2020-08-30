#!make
.PHONY := help push lint build dev

.DEFAULT_GOAL := dev

BIN := ingress

GO_DIR := $(shell find . -type f -name '*.go' | cut -d "/" -f2 | head -n 1)

help: ## List of defined target
	@grep -E '^[a-zA-Z_-]+:.*?##.*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'	

build: ## Go build ingress
	cd $(GO_DIR) && swagger generate spec -o docs/ui/dist/swagger.json
	cd $(GO_DIR)/docs && statik -src ui/dist -p ui -f
	cd $(GO_DIR) && go build -o bin/$(BIN) .

lint: ## Go lint
	cd $(GO_DIR) && golangci-lint run

ingress-run: ## Run ingress
	cd $(GO_DIR) && go run .

ingress-dev: ## Run ingress (with reflex to reload when detected changes)
	ulimit -n 1000
	reflex --decoration=fancy -s -r '\.go$$' $(MAKE) ingress-run

pr-dev: ## runs python inference server with FastAPI
	uvicorn price_recommender.main:app --workers 8 --reload --port 5000

dev: build ## run both watch-pr and watch-ingress
	$(MAKE) -j 2 pr-dev ingress-dev 

docker-%: ## build, run, push with configuration
	docker-compose -f deploy/docker-compose.yml $*

push: ## build and then push images to registry
	$(MAKE) docker-build && $(MAKE) docker-push
