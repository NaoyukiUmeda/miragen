# MIRAGEN Website

株式会社MIRAGENの公式Webサイト

## デプロイ方法

### Cloudflare Pages
```bash
npx wrangler deploy
```

### ローカル開発
```bash
python -m http.server 8000
```

## ファイル構成
```
.
├── index.html          # メインHTMLファイル
├── styles.css          # スタイルシート
├── script.js           # JavaScript
├── assets/
│   ├── images/        # 画像ファイル
│   └── css/           # フォントCSS
└── wrangler.jsonc     # Cloudflare Pages設定
```

## 技術スタック
- HTML5
- CSS3 (アニメーション、グラデーション、レスポンシブ)
- Vanilla JavaScript
- Google Fonts (Montserrat, Noto Sans JP)

## ライセンス
© 2024 MIRAGEN Inc.
