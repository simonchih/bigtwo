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

中文介面使用內附的 Noto Sans CJK TC 繁體中文字型，Windows、macOS 與 Linux 均不需另外安裝字型。字型來源為 [Noto CJK](https://github.com/notofonts/noto-cjk/tree/Sans2.004)，授權文件位於 `fonts/OFL.txt`。舊 `dist/main.exe` 是原版封存，不含本次修改；請使用 `play.bat` 或新版原始碼啟動。

## 驗證與重建

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe main.py --headless --autoplay --frames 180 --screenshot art/gameplay.png
# 僅重建素材時需要 Pillow
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe tools/build_assets.py
```

路徑均相對程式所在位置解析，可從其他工作目錄啟動。遊戲不需要網路或 API 金鑰。


## 一鍵建置單一 EXE（Windows）

雙擊 `build.bat`，成功後會產生 `dist/BigTwo.exe`。圖片與備用字型已全部封裝，分享時只需複製這一個 EXE，不需要另外附上 Image 資料夾或安裝 Python。

建置電腦需安裝 Python 3.10 以上；第一次執行需要網路下載依賴。腳本自動建立獨立的 `.build-venv`，不影響遊戲的 `.venv`。建置失敗會顯示錯誤並停留在視窗，成功則顯示輸出路徑。可重複執行更新 EXE。

自動化環境可使用 `build.bat --no-pause`，成功回傳 0、失敗回傳 1。`BigTwo.spec` 定義單檔、無主控台視窗、內嵌圖示與素材的封裝設定。遊戲規則不受建置影響。

單檔 EXE 啟動時會自動將內嵌資源解壓到系統暫存目錄，因此第一次啟動可能稍慢；不會要求使用者手動解壓。繁體中文字型與授權文件也已內嵌。

macOS / Linux 使用 `./build.sh` 建置。腳本同樣會建立 `.build-venv`、安裝 `requirements-build.txt`，完成後執行 `./dist/BigTwo`。可用 `PYTHON=/path/to/python3 ./build.sh` 指定建立環境的 Python。

兩個建置腳本均會清除 PyInstaller 快取後重新封裝。缺少繁體中文字型或授權文件時會停止建置，避免產生無法顯示中文的執行檔。執行檔僅適用於建置時的作業系統與 CPU 架構；Windows EXE 需在 Windows 上建置。
