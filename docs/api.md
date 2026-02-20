# API エンドポイント

## 📡 API エンドポイント一覧

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/health` | ヘルスチェック |
| GET | `/api/v1/projects` | プロジェクト一覧 |
| POST | `/api/v1/projects` | プロジェクト作成 |
| GET | `/api/v1/projects/{id}` | プロジェクト詳細 |
| PATCH | `/api/v1/projects/{id}` | プロジェクト更新 |
| DELETE | `/api/v1/projects/{id}` | プロジェクト削除 |
| GET | `/api/v1/projects/{id}/tasks` | タスク一覧 |
| POST | `/api/v1/projects/{id}/tasks` | タスク作成 |
| PATCH | `/api/v1/projects/{id}/tasks/{task_id}` | タスク更新 |
| DELETE | `/api/v1/projects/{id}/tasks/{task_id}` | タスク削除 |

詳細なAPI仕様は、ローカル環境（`docker compose up -d`）起動後に以下からアクセスできる Swagger UI で確認できます：
[http://localhost:8000/docs](http://localhost:8000/docs)
