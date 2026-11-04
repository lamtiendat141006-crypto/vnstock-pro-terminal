@echo off
chcp 65001 >nul
echo ============================================================================
echo   ĐẨY DỰ ÁN VNSTOCK PRO LÊN GITHUB CÁ NHÂN (CHUẨN PORTFOLIO CV)
echo ============================================================================
echo [!] Lưu ý: File .env chứa khóa API SSI của bạn đã được .gitignore bảo vệ,
echo     chỉ đẩy code sạch và .env.example lên GitHub.
echo.
set /p REPO_URL="Nhập link GitHub Repository của bạn (VD: https://github.com/username/vnstock-pro-terminal.git): "
if "%REPO_URL%"=="" (
    echo [X] Bạn chưa nhập link GitHub Repository!
    pause
    exit /b 1
)

git init
git add .
git commit -m "feat: Initial release of VNStock Pro TradingView Terminal & Financial ML Analytics"
git branch -M main
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git push -u origin main

echo.
echo ============================================================================
echo ✅ ĐÃ ĐẨY CODE LÊN GITHUB THÀNH CÔNG!
echo 👉 Hãy vào tab Settings -> Pages trên GitHub, chọn Source: "GitHub Actions"
echo    để có ngay link Live Demo gắn vào CV xin việc!
echo ============================================================================
pause
