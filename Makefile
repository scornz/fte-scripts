.PHONY:install hooks clean

bold := $(shell tput bold)
red := $(shell tput setaf 1)
green := $(shell tput setaf 2)
blue := $(shell tput setaf 4)
reset := $(shell tput sgr0)

setup: install hooks
	@printf '${green}${bold}Sucessfully set up${reset} fte-scripts!\n'

install:
	@printf '${green}${bold}Installing dependencies${reset}...\n'
	pipenv install

hooks:
	@printf '${green}${bold}Setting up hooks${reset}...\n'
	pipenv run pre-commit autoupdate
	pipenv run pre-commit install
	pipenv run pre-commit install --hook-type commit-msg

clean:
	@printf '${red}${bold}Cleaning${reset}...\n'
	@printf '${red}Removing hooks${reset}...\n'
	rm .git/hooks/pre-commit
	rm .git/hooks/commit-msg