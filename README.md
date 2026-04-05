@echo off
python -m pip install -U pip nuitka pyarmor zstandard cryptography pillow keyboard
python -m pyarmor.cli gen --non-runtime D1_Bypass.py
cd dist
python -m nuitka --standalone --onefile --windows-uac-admin --windows-disable-console --enable-plugin=tk-inter --include-package=PIL --include-package=cryptography --output-dir=../final_build D1_Bypass.py
echo [OK] Build hoàn tất! Kiểm tra thư mục final_build.
