#!/usr/bin/env bash
echo "============================================================================"
echo "  ĐẨY DỰ ÁN VNSTOCK PRO LÊN GITHUB CÁ NHÂN (CHUẨN PORTFOLIO CV)"
echo "============================================================================"
read -p "Nhập link GitHub Repository của bạn (VD: https://github.com/username/vnstock-pro-terminal.git): " REPO_URL
if [ -z "$REPO_URL" ]; then
  echo "[X] Bạn chưa nhập link GitHub Repository!"
  exit 1
fi

git init
git add .
git commit -m "feat: Initial release of VNStock Pro TradingView Terminal & Financial ML Analytics"
git branch -M main
git remote remove origin 2>/dev/null
git remote add origin "$REPO_URL"
git push -u origin main
echo "✅ ĐÃ ĐẨY CODE LÊN GITHUB THÀNH CÔNG!"
