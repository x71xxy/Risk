@echo off
call venv\Scripts\activate
python -m pytest --cov=app --cov-report=term-missing
pause 