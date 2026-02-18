/**
 * API クライアント
 *
 * fetch ベースの HTTP クライアント。
 * バックエンドの RESTful API と通信する。
 * 環境変数で API ベース URL を切り替え可能。
 */

import type {
    Project,
    ProjectCreate,
    ProjectUpdate,
    Task,
    TaskCreate,
    TaskUpdate,
    PaginatedResponse,
    HealthCheck,
} from '$lib/types';

/**
 * API ベース URL
 *
 * SvelteKit の環境変数（PUBLIC_ プレフィックス）から取得。
 * Vite プロキシ経由の場合は空文字列（相対パス）でOK。
 */
const API_BASE = '';

/**
 * API リクエストを実行する共通関数
 *
 * エラーハンドリングとJSONパースを一元管理。
 */
async function request<T>(
    path: string,
    options: RequestInit = {},
): Promise<T> {
    const url = `${API_BASE}${path}`;

    const response = await fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
        ...options,
    });

    // 204 No Content の場合はボディなし
    if (response.status === 204) {
        return undefined as T;
    }

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || `API Error: ${response.status}`);
    }

    return response.json();
}

// ============================================
// ヘルスチェック
// ============================================

/** ヘルスチェック API を呼び出す */
export async function getHealth(): Promise<HealthCheck> {
    return request<HealthCheck>('/health');
}

// ============================================
// プロジェクト API
// ============================================

/** プロジェクト一覧を取得（ページネーション付き） */
export async function getProjects(
    page: number = 1,
    perPage: number = 20,
): Promise<PaginatedResponse<Project>> {
    return request<PaginatedResponse<Project>>(
        `/api/v1/projects?page=${page}&per_page=${perPage}`,
    );
}

/** 指定IDのプロジェクトを取得 */
export async function getProject(id: string): Promise<Project> {
    return request<Project>(`/api/v1/projects/${id}`);
}

/** 新しいプロジェクトを作成 */
export async function createProject(data: ProjectCreate): Promise<Project> {
    return request<Project>('/api/v1/projects', {
        method: 'POST',
        body: JSON.stringify(data),
    });
}

/** プロジェクトを部分更新 */
export async function updateProject(
    id: string,
    data: ProjectUpdate,
): Promise<Project> {
    return request<Project>(`/api/v1/projects/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
    });
}

/** プロジェクトを削除 */
export async function deleteProject(id: string): Promise<void> {
    return request<void>(`/api/v1/projects/${id}`, {
        method: 'DELETE',
    });
}

// ============================================
// タスク API
// ============================================

/** プロジェクトのタスク一覧を取得 */
export async function getTasks(
    projectId: string,
    page: number = 1,
    perPage: number = 20,
): Promise<PaginatedResponse<Task>> {
    return request<PaginatedResponse<Task>>(
        `/api/v1/projects/${projectId}/tasks?page=${page}&per_page=${perPage}`,
    );
}

/** 新しいタスクを作成 */
export async function createTask(
    projectId: string,
    data: TaskCreate,
): Promise<Task> {
    return request<Task>(`/api/v1/projects/${projectId}/tasks`, {
        method: 'POST',
        body: JSON.stringify(data),
    });
}

/** タスクを部分更新 */
export async function updateTask(
    projectId: string,
    taskId: string,
    data: TaskUpdate,
): Promise<Task> {
    return request<Task>(`/api/v1/projects/${projectId}/tasks/${taskId}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
    });
}

/** タスクを削除（論理削除） */
export async function deleteTask(
    projectId: string,
    taskId: string,
): Promise<void> {
    return request<void>(`/api/v1/projects/${projectId}/tasks/${taskId}`, {
        method: 'DELETE',
    });
}
