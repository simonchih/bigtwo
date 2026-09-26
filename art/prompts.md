# 美術生成紀錄

使用內建 image_gen，參考使用者提供的 bigtwo_icon.png。

## 桌面：Image/table.png

Use case: style-transfer. Asset type: full-screen background for a 1280x720 Pygame Big Two card game. Use attached image as material and style reference only. Create a wide 16:9 top-down empty luxury emerald-green felt card table. Rich fine felt texture, subtle radial pool of green light in center, dark forest-green corners. Thin elegant rounded rectangular polished gold double rail close to outer edges, small delicate gold diamond ornaments centered on left and right rails. Large completely empty unobstructed playing area, no cards, no crown in center, no text, no people, no buttons, no UI. Match reference's warm metallic highlights and tactile luxurious material. Flat orthographic view, tasteful understated lighting suitable for readable game overlays. Save generated image to workspace if possible.

## 牌背：Image/card_back.png

Use case: style-transfer. Asset type: playing card back for Pygame game, based on the emerald felt and polished gold style of reference. One single vertical playing card back, perfectly rectangular 2:3 aspect card occupying entire portrait image, rounded corners, orthographic front view, no perspective. Deep emerald leather textured inset, fine symmetrical gold guilloche diamond lattice, elegant double ivory and metallic gold rim, a small ornate golden crown centered inside a gold diamond medallion. Symmetric 180 degree design. No words, letters, numbers, extra objects, hands, shadows outside card or backdrop. Highly refined tactile premium casino asset, sharp detail.

牌面數字、花色與輔助 UI 為 theme.py 原生程式繪圖，tools/build_assets.py 匯出 PNG 與舊格式相容版本。圖示取自使用者提供的圖片。

