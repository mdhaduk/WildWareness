# get git config
config:
	git config -l

# get git status
status:
	make --no-print-directory clean
	@echo
	git branch
	git remote -v
	git status

# download files from the code repo
pull:
	make --no-print-directory clean
	@echo
	git pull
	git status

# upload files to the Grades code repo
push:
	make --no-print-directory clean
	@echo
	git add .gitignore
	git add .gitlab-ci.yml
	git add frontend
	git add Makefile
	git add README.md
	git add scripts
	git add .env
	git commit -m "another commit"
	git push
	git status

# checks to see that gitignore and the pipeline file are present
check: .gitignore .gitlab-ci.yml