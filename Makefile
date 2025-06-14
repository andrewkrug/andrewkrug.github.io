ROOT_DIR	:= $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

all:
	@echo 'Available make targets:'
	@grep '^[^#[:space:]^\.PHONY.*].*:' Makefile

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
	npm run serve
	@echo 'The site is now being served at http://localhost:8080'

.PHONY: build
build: clean setup
	cd _site && git checkout master
	hugo -D
	@echo 'The site is now ready to deploy within /public.'

.PHONY: deploy
deploy: build
	@echo 'Attempting a deploy to master'
	cp CNAME _site/
	cp README.md _site/
	cp favicon.ico _site/
	cd public && git add -A
	cd public &&  git commit -m 'Updated site.  See gh-pages branch for detailed info'
	cd public && git push origin master
	@echo 'deploy complete to master branch'