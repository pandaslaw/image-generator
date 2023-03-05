@echo off

python -m virtualenv venv
call venv\Scripts\activate.bat

pip install -r requirements.txt
python -m uvicorn src.main:app --port 5000
