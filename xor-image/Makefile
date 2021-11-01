lint: 
	autoflake --in-place --recursive --ignore-init-module-imports --remove-duplicate-keys --remove-unused-variables --remove-all-unused-imports src
	black src
	isort src
	mypy src 