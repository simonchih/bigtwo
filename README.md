# 大老二 · Emerald Crown

以翡翠綠絨布、金色皇冠與奶油白牌面重新設計的 Pygame 大老二。

## 執行

Windows 可直接雙擊 `play.bat`。本專案已建立 `.venv`；另台電腦請使用 Python 3.10 以上：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

左鍵選牌；Enter 出牌、Space 略過、H 提示、R 重新開局、F1 規則、Esc 關閉規則或離開遊戲。保留右鍵出牌／未選牌時略過的操作。支援視窗縮放與等比例顯示。

## 規則

延續原專案台灣規則：梅花 3 先出，2 最大、3 最小；花色梅花 < 方塊 < 紅心 < 黑桃。
支援單張、對子、順子、葫蘆、鐵支、同花順、一條龍／同花一條龍。
**葫蘆不能壓順子，順子也不能壓葫蘆；不能單獨出三條。** 普通同花不是合法牌型。
A2345 為最小順子、23456 最大；同型順子比最大牌，A2345 比 5。
鐵支／同花順可壓順子與葫蘆，也可跨張數壓單張與對子；同花順大於鐵支，一條龍可壓其他牌型。
略過者本輪不再出牌；另外三家略過後，最後出牌者重新領牌。發牌行為依原始程式，不額外加入四張 2 自動重洗。

## 美術與程式

- `Image/`：原有 124 張圖片全部替換；新增 52 張 PNG 牌面、AI 製作的桌面與牌背。圖示使用使用者提供的圖片。
- `main.py`：60 FPS 上限、非阻塞 AI 節奏、發牌動畫、選牌浮起、出牌飛行、金色粒子與勝利畫面。
- `original_rules.py`：直接保留原始程式的牌型與比較函式，固定 Taiwan 模式。
- `game.py`：回合管理與 AI 呼叫原始規則，不另行定義牌型大小。
- `theme.py`、`tools/build_assets.py`：精確繪製數字／花色與匯出相容素材。
- `art/`：畫面截圖、生成提示詞與原程式封存。

中文字型優先使用 Windows 微軟正黑體，Linux 可安裝 Noto Sans CJK 或 WenQuanYi Zen Hei。舊 `dist/main.exe` 是原版封存，不含本次修改；請使用 `play.bat` 或新版原始碼啟動。

## 驗證與重建

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe main.py --headless --autoplay --frames 180 --screenshot art/gameplay.png
# 僅重建素材時需要 Pillow
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe tools/build_assets.py
```

路徑均相對程式所在位置解析，可從其他工作目錄啟動。遊戲不需要網路或 API 金鑰。
