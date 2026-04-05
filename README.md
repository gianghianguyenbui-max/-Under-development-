@echo off
:: 1. Cai dat thu vien bang python -m pip de dam bao khong loi PATH
python -m pip install -U pip
python -m pip install -U nuitka pyarmor zstandard cryptography pillow keyboard

:: 2. Chay Pyarmor bang python -m de ma hoa code
:: Luu y: Pyarmor 8.x tro len thuong dung 'gen' truc tiep hoac qua python -m pyarmor.cli
python -m pyarmor.cli gen --non-runtime D1_Bypass.py

:: 3. Di chuyen vao thu muc chua file da ma hoa
cd dist

:: 4. Build bang Nuitka voi day du cac flag ong can
:: Dung python -m nuitka de chac chan goi dung compiler
python -m nuitka --standalone --onefile --windows-uac-admin --windows-disable-console --enable-plugin=tk-inter --include-package=PIL --include-package=cryptography --output-dir=../final_build D1_Bypass.py

echo [OK] Build xong roi do ong chau! Check thu muc final_build di.
pause

