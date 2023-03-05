@echo off

call venv\Scripts\activate.bat

pytest tests

call venv\Scripts\deactivate.bat
