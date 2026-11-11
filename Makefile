ROOT_DIR	:= $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

all:
	@echo 'Available make targets:'
	@grep '^[^#[:space:].A-Z].*:' Makefile

.PHONY: setup
setup: 
	@echo 'Installing node modules'
	npm install

.PHONY: clean
clean:
	@echo 'Blowing away old builds'
	rm -rf _site/*

.PHONY: preview
preview:
	@echo 'The site is now being served at http://localhost:8080'
	npm run serve

.PHONY: run
run: preview

.PHONY: build
build: clean setup
	npm run build
	@echo 'Site built to _site/. Deploys happen via .github/workflows/release.yml on push to main.'