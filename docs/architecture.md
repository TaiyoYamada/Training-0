# プロジェクト構成詳細

## 📁 ディレクトリ構造

<details open>
<summary>backend/</summary>

```
backend/
├── app/
│   ├── api/routes/          # API ルート定義
│   ├── core/config.py       # 環境設定（dev/staging/prod）
│   ├── db/                  # DB セッション + DI
│   ├── models/              # SQLAlchemy モデル
│   ├── repositories/        # データアクセス層
│   ├── schemas/             # Pydantic スキーマ
│   ├── services/            # ビジネスロジック
│   └── main.py              # エントリーポイント
├── alembic/                 # マイグレーション
├── Dockerfile               # マルチステージビルド
└── pyproject.toml           # uv プロジェクト定義
```
</details>

<details open>
<summary>frontend/</summary>

```
frontend/
├── src/
│   ├── lib/
│   │   ├── api/client.ts    # fetch ベース API クライアント
│   │   ├── types/index.ts   # TypeScript 型定義
│   │   └── components/      # 共通コンポーネント
│   └── routes/
│       ├── +layout.svelte   # 共通レイアウト
│       ├── +page.svelte     # プロジェクト一覧
│       └── projects/[id]/   # プロジェクト詳細
├── Dockerfile               # マルチステージ（dev/production）
├── svelte.config.js
└── package.json
```
</details>
