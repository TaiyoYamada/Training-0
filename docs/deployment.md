# デプロイと CI/CD

## 🏭 本番デプロイ

```bash
# 本番用 docker-compose で起動
docker compose -f infra/docker/production-compose.yml up --build -d
```

本番構成では Nginx リバースプロキシが 80 番ポートで全トラフィックを処理し、
`/api/` → バックエンド、それ以外 → フロントエンドにルーティングします。

## 🔄 CI/CD

| ワークフロー | トリガー | 内容 |
|-------------|---------|------|
| `backend.yml` | push / PR（backend/ 変更時） | Ruff lint → Mypy → Pytest |
| `docker.yml` | push to main | Docker イメージビルド + SHA タグ |
