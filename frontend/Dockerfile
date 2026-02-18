# ===========================================
# Training-0 フロントエンド Dockerfile
# SvelteKit + Node.js
# マルチステージビルド（dev / production）
# ===========================================

# =========================================
# ステージ1: 依存関係インストール
# =========================================
FROM node:22-slim AS deps

WORKDIR /app

# package.json のみを先にコピー（キャッシュ活用）
COPY package.json ./

# 依存関係をインストール
RUN npm install

# =========================================
# ステージ2: 開発サーバー（docker-compose 用）
# =========================================
FROM node:22-slim AS dev

WORKDIR /app

# 依存関係をコピー
COPY --from=deps /app/node_modules ./node_modules
COPY . .

EXPOSE 5173

# SvelteKit 開発サーバーを起動
CMD ["npm", "run", "dev"]

# =========================================
# ステージ3: ビルド（本番用）
# =========================================
FROM node:22-slim AS build

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# 本番ビルド
RUN npm run build

# =========================================
# ステージ4: 本番ランタイム
# =========================================
FROM node:22-slim AS production

# 非rootユーザーの作成
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home appuser

WORKDIR /app

# ビルド成果物のみをコピー（最小イメージ）
COPY --from=build /app/build ./build
COPY --from=build /app/package.json ./

# 本番用依存関係のみインストール
RUN npm install --omit=dev

# 非rootユーザーに切り替え
USER appuser

EXPOSE 3000

# Node.js サーバーで起動
CMD ["node", "build"]
