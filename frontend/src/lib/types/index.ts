/**
 * TypeScript 型定義
 *
 * バックエンドの Pydantic スキーマに対応する型を定義。
 * Codable（JSON シリアライズ/デシリアライズ）に対応。
 */

/** プロジェクト型（レスポンス） */
export interface Project {
    id: string;
    name: string;
    description: string | null;
    created_at: string;
    updated_at: string;
}

/** プロジェクト作成リクエスト */
export interface ProjectCreate {
    name: string;
    description?: string | null;
}

/** プロジェクト更新リクエスト */
export interface ProjectUpdate {
    name?: string;
    description?: string | null;
}

/** タスクステータス */
export type TaskStatus = 'todo' | 'in_progress' | 'done';

/** タスク型（レスポンス） */
export interface Task {
    id: string;
    project_id: string;
    title: string;
    description: string | null;
    status: TaskStatus;
    priority: number;
    due_date: string | null;
    is_deleted: boolean;
    created_at: string;
    updated_at: string;
}

/** タスク作成リクエスト */
export interface TaskCreate {
    title: string;
    description?: string | null;
    status?: TaskStatus;
    priority?: number;
    due_date?: string | null;
}

/** タスク更新リクエスト */
export interface TaskUpdate {
    title?: string;
    description?: string | null;
    status?: TaskStatus;
    priority?: number;
    due_date?: string | null;
}

/** ページネーション付きレスポンス */
export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    per_page: number;
    pages: number;
}

/** ヘルスチェックレスポンス */
export interface HealthCheck {
    status: string;
    database: string;
    version: string;
}
