@echo off


:start
cls

set python_ver=37

python ./get-pip.py

cd \
cd \python%python_ver%\Scripts\
pip install pywebio
pip install pyperclip

pause
exit