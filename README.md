# 📈 VNStock Pro Terminal — Vietnamese Stock Market TradingView & Financial Machine Learning Platform

![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![HTML5 Canvas](https://img.shields.io/badge/Chart_Engine-HTML5_Canvas_2D-E34F26?logo=html5&logoColor=white)
![SSI FastConnect API](https://img.shields.io/badge/Market_Data-SSI_FastConnect_v2.0-00A651)
![CafeF EOD](https://img.shields.io/badge/EOD_Dataset-CafeF_Verified-2962FF)
![License MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

> **FinTech & Quantitative Data Mining Project**: An interactive multi-pane technical analysis terminal (inspired by TradingView & SSI iBoard), sector liquidity treemap heatmap, and in-browser financial machine learning suite built for the Vietnamese stock market (**HOSE, HNX, UPCOM, VN30**).

---

## 🌟 Điểm nhấn Kỹ thuật (Key Engineering Highlights)

1. **Multi-Pane HTML5 Canvas Charting Engine (Zero External Charting Dependencies)**:
   - Custom high-DPI `<canvas>` rendering engine supporting **Japanese Candlesticks**, **OHLC Bars**, **Heikin-Ashi**, and **Area Charts** coupled with **Volume Histograms** and interactive drawing tools (*Trendlines, Horizontal Support/Resistance, Fibonacci Retracement, Price Range Ruler*).
   - Real-time calculation of overlay & oscillator indicators: **SMA (3, 5, 10)**, **EMA**, **Bollinger Bands (20, 2σ)**, **VWAP**, **RSI**, **MACD**, **ROC**, and **Volume Z-Score**.

2. **End-to-End EOD Data Cleaning & Corporate Action Adjustment Pipeline**:
   - Ingests raw MetaStock/AmiBroker CSV files (`<Ticker>,<DTYYYYMMDD>,<Open>,<High>,<Low>,<Close>,<Volume>`) from [CafeF Historical Data](https://cafef.vn/du-lieu/du-lieu-download.chn) and live streams from [SSI FastConnect Data API v2.0](https://guide.ssi.com.vn/ssi-products/fastconnect-data/api-specs).
   - **Automated Corporate Action Split Normalization**: Detects and adjusts pre-split historical prices (e.g., normalizing `TCB`'s technical reference adjustment on `29/10/2026` with factor `k = 0.6672`) so technical indicators and ML features are never distorted by artificial price gaps.

3. **Financial Machine Learning & Quantitative Data Mining**:
   - **K-Means Clustering**: Unsupervised clustering of listed equities across 3 dimensions (*10-Day Return %, Daily Volatility σ%, and Matched Liquidity*) into actionable market regimes.
   - **Z-Score Volume & Price Anomaly Scanner**: Automated detection of institutional volume breakouts ($Z > 1.5\sigma$) and ceiling/floor limit moves.
   - **Multi-Asset Pearson Correlation Matrix**: Real-time return correlation matrix across `VN-Index`, `VN30`, and sector leaders to support Markowitz portfolio diversification.

4. **Hybrid Real-Time Architecture & Security**:
   - Built-in Python `ThreadingHTTPServer` reverse proxy (`server_localhost.py`) that loads credentials (`SSI_CONSUMER_ID`, `SSI_CONSUMER_SECRET`, `SSI_PRIVATE_KEY`) securely from local `.env` (protected by `.gitignore`) and relays requests to `https://fc-data.ssi.com.vn/api/v2/Market` with zero browser CORS blocks.
   - Pre-loaded with **64+ verified tickers & indices** (including **100% of the VN30 basket** and over **600 verified EOD records** from CafeF) plus on-demand fetching for **1,600+ stocks** across HOSE, HNX, and UPCOM.

---

## 🚀 Hướng dẫn Khởi chạy Nhanh (Quick Start on Localhost)

### 1. Clone dự án & cấu hình biến môi trường
```bash
git clone https://github.com/<your-username>/vnstock-pro-terminal.git
cd vnstock-pro-terminal
cp .env.example .env
# Điền SSI_CONSUMER_ID, SSI_CONSUMER_SECRET, SSI_PRIVATE_KEY của bạn vào file .env
```

### 2. Khởi chạy máy chủ Localhost (Port 8080)
```bash
python server_localhost.py
```
Trình duyệt sẽ tự động mở tại địa chỉ **`http://localhost:8080`**.

---

## 💼 Gợi ý Mô tả Dự án trong CV (Ready-to-Use CV Bullet Points)

Bạn có thể sao chép trực tiếp phần mô tả dưới đây vào mục **Projects (Dự án cá nhân / Dự án học thuật)** trong CV ứng tuyển các vị trí **Data Analyst, Financial Data Scientist, Quantitative Developer, FinTech Software Engineer**:

### Bản Tiếng Việt (Dành cho CV Tiếng Việt)
**VNStock Pro Terminal — Nền tảng Phân tích Kỹ thuật & Khai phá Dữ liệu Chứng khoán Việt Nam**
*Vai trò: Full-stack FinTech Developer & Data Analyst | Công nghệ: Python, JavaScript (ES6+), HTML5 Canvas, Tailwind CSS, SSI FastConnect REST API, CafeF EOD*
- **Xây dựng Pipeline ETL & Làm sạch dữ liệu tài chính**: Thu thập và chuẩn hóa hơn 600+ bản ghi EOD từ CafeF và SSI FastConnect API (100% rổ VN30 và các mã dẫn đầu HOSE/HNX/UPCOM); thiết kế thuật toán tự động phát hiện và hiệu chỉnh nhảy giá do chia tách cổ phiếu/cổ tức (Corporate Action Adjustment), loại bỏ nhiễu dữ liệu cho mô hình định lượng.
- **Phát triển Giao diện Biểu đồ TradingView & Bản đồ nhiệt (Treemap Heatmap)**: Lập trình trực tiếp engine đồ thị đa khung bằng HTML5 Canvas (Nến Nhật, Heikin-Ashi, OHLC, Volume, Fibonacci, SMA/EMA, Bollinger Bands, RSI, MACD) và bản đồ nhiệt dòng tiền theo nhóm ngành chuẩn bảng điện tử HOSE.
- **Triển khai Thuật toán Học máy Tài chính (Financial Machine Learning)**: Cài đặt thuật toán phân cụm không giám sát **K-Means** phân loại cổ phiếu theo Khẩu vị Rủi ro – Lợi suất – Thanh khoản, bộ quét bất thường **Z-Score Volume Breakout**, và **Ma trận tương quan Pearson** phục vụ tối ưu hóa danh mục đầu tư.
- **Thiết kế Kiến trúc Reverse Proxy & Tự động hóa CI/CD**: Xây dựng máy chủ Python Localhost tích hợp CORS Relay bảo mật khóa RSA/API qua biến môi trường (`.env`) và triển khai tự động Live Demo qua GitHub Pages.

### English Version (For International / English Resume)
**VNStock Pro Terminal — Real-Time Vietnamese Equity Analytics & Financial Machine Learning Platform**
*Role: FinTech Developer & Quantitative Data Analyst | Stack: Python, Vanilla JS, HTML5 Canvas, Tailwind CSS, SSI FastConnect API v2.0*
- **Engineered Financial EOD ETL & Corporate Action Pipeline**: Processed 600+ verified EOD records across 64+ Vietnamese equities (100% of the VN30 index basket) from CafeF and SSI FastConnect API; implemented automated split/dividend adjustment factors to eliminate artificial price gaps.
- **Built Custom Multi-Pane TradingView Chart Engine & Sector Treemap**: Developed a dependency-free HTML5 Canvas charting engine supporting Candlesticks, Heikin-Ashi, interactive Fibonacci/Trendline overlays, and 8+ technical indicators alongside a real-time HOSE/HNX/UPCOM market liquidity heatmap.
- **Implemented In-Browser Financial Machine Learning Suite**: Deployed **K-Means Clustering** (Risk-Return-Liquidity regime segmentation), **Z-Score Anomaly Detection** for institutional volume breakouts, and a **Multi-Asset Pearson Correlation Matrix** for portfolio risk analysis.
