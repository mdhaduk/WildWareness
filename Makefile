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

# upload files to the code repo
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

# Run Python backend tests
test-backend:
	cd backend && source ./venv/bin/activate && python run_tests.py

# Run JavaScript frontend tests
test-frontend:
	cd frontend && npm test

# Run Selenium tests
test-selenium:
	cd frontend && python frontendAcceptanceTests.py

# Run all tests
test: test-backend test-frontend test-selenium
	@echo "All tests completed"

# Clean any generated files
clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name ".pytest_cache" -type d -exec rm -rf {} +