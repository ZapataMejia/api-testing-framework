.PHONY: install test test-smoke test-regression test-performance test-schema report lint format clean

install:
	pip install -r requirements.txt

test:
	pytest --html=report.html --self-contained-html

test-smoke:
	pytest -m smoke --html=report-smoke.html --self-contained-html

test-regression:
	pytest -m regression --html=report-regression.html --self-contained-html

test-performance:
	pytest -m performance --html=report-performance.html --self-contained-html

test-schema:
	pytest -m schema --html=report-schema.html --self-contained-html

test-parallel:
	pytest -n auto --html=report.html --self-contained-html

report:
	pytest --alluredir=allure-results
	allure serve allure-results

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

clean:
	rm -rf __pycache__ .pytest_cache allure-results allure-report htmlcov *.html
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
