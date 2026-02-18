<!--
  プロジェクト一覧ページ（トップページ）

  - プロジェクトの一覧表示
  - 新規プロジェクト作成フォーム
  - プロジェクト削除
-->
<script lang="ts">
    import { getProjects, createProject, deleteProject } from "$lib/api/client";
    import type { Project, ProjectCreate } from "$lib/types";

    // --- Svelte 5 リアクティブ state ---
    let projects = $state<Project[]>([]);
    let loading = $state(true);
    let error = $state<string | null>(null);

    // 新規作成フォーム
    let showForm = $state(false);
    let newName = $state("");
    let newDescription = $state("");
    let creating = $state(false);

    // プロジェクト一覧を取得
    async function loadProjects() {
        loading = true;
        error = null;
        try {
            const response = await getProjects();
            projects = response.items;
        } catch (e) {
            error = e instanceof Error ? e.message : "読み込みに失敗しました";
        } finally {
            loading = false;
        }
    }

    // プロジェクトを新規作成
    async function handleCreate() {
        if (!newName.trim()) return;
        creating = true;
        try {
            const data: ProjectCreate = {
                name: newName.trim(),
                description: newDescription.trim() || null,
            };
            await createProject(data);
            newName = "";
            newDescription = "";
            showForm = false;
            await loadProjects();
        } catch (e) {
            error = e instanceof Error ? e.message : "作成に失敗しました";
        } finally {
            creating = false;
        }
    }

    // プロジェクトを削除
    async function handleDelete(id: string) {
        if (
            !confirm(
                "このプロジェクトを削除しますか？関連するタスクも削除されます。",
            )
        )
            return;
        try {
            await deleteProject(id);
            await loadProjects();
        } catch (e) {
            error = e instanceof Error ? e.message : "削除に失敗しました";
        }
    }

    // 日付フォーマット
    function formatDate(dateStr: string): string {
        return new Date(dateStr).toLocaleDateString("ja-JP", {
            year: "numeric",
            month: "short",
            day: "numeric",
        });
    }

    // 初回ロード
    $effect(() => {
        loadProjects();
    });
</script>

<svelte:head>
    <title>プロジェクト一覧 | Training-0</title>
</svelte:head>

<div class="container">
    <!-- ページヘッダー -->
    <div class="page-header">
        <div>
            <h1 class="page-title">プロジェクト</h1>
            <p class="page-subtitle">プロジェクトの管理と追跡</p>
        </div>
        <button class="btn btn-primary" onclick={() => (showForm = !showForm)}>
            {showForm ? "✕ キャンセル" : "＋ 新規作成"}
        </button>
    </div>

    <!-- エラー表示 -->
    {#if error}
        <div class="alert alert-error">
            <span>⚠️ {error}</span>
            <button class="btn btn-sm btn-ghost" onclick={() => (error = null)}
                >✕</button
            >
        </div>
    {/if}

    <!-- 新規作成フォーム -->
    {#if showForm}
        <div class="card create-form" style="margin-bottom: var(--space-6);">
            <h2 class="form-title">新しいプロジェクト</h2>
            <form
                onsubmit={(e) => {
                    e.preventDefault();
                    handleCreate();
                }}
            >
                <div class="form-group">
                    <label for="project-name" class="label"
                        >プロジェクト名 *</label
                    >
                    <input
                        id="project-name"
                        class="input"
                        type="text"
                        bind:value={newName}
                        placeholder="例：マイプロジェクト"
                        required
                    />
                </div>
                <div class="form-group">
                    <label for="project-desc" class="label">説明（任意）</label>
                    <textarea
                        id="project-desc"
                        class="textarea"
                        bind:value={newDescription}
                        placeholder="プロジェクトの概要を入力..."
                    ></textarea>
                </div>
                <div class="form-actions">
                    <button
                        type="submit"
                        class="btn btn-primary"
                        disabled={creating || !newName.trim()}
                    >
                        {creating ? "作成中..." : "作成"}
                    </button>
                </div>
            </form>
        </div>
    {/if}

    <!-- ローディング -->
    {#if loading}
        <div class="loading">
            <div class="spinner"></div>
            <p>読み込み中...</p>
        </div>
    {:else if projects.length === 0}
        <!-- 空状態 -->
        <div class="empty-state">
            <p class="empty-icon">📁</p>
            <p class="empty-text">プロジェクトがありません</p>
            <p class="empty-hint">
                「新規作成」ボタンから最初のプロジェクトを作成しましょう
            </p>
        </div>
    {:else}
        <!-- プロジェクト一覧 -->
        <div class="project-list">
            {#each projects as project (project.id)}
                <a href="/projects/{project.id}" class="card project-card">
                    <div class="project-info">
                        <h3 class="project-name">{project.name}</h3>
                        {#if project.description}
                            <p class="project-desc">{project.description}</p>
                        {/if}
                        <p class="project-meta">
                            作成日: {formatDate(project.created_at)}
                        </p>
                    </div>
                    <div class="project-actions">
                        <button
                            class="btn btn-sm btn-danger"
                            onclick={(e) => {
                                e.preventDefault();
                                handleDelete(project.id);
                            }}
                        >
                            削除
                        </button>
                    </div>
                </a>
            {/each}
        </div>
    {/if}
</div>

<style>
    .page-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        margin-bottom: var(--space-8);
    }

    .page-title {
        font-size: var(--font-size-3xl);
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    .page-subtitle {
        color: var(--color-text-secondary);
        margin-top: var(--space-1);
    }

    .form-title {
        font-size: var(--font-size-lg);
        font-weight: 600;
        margin-bottom: var(--space-5);
    }

    .form-group {
        margin-bottom: var(--space-4);
    }

    .label {
        display: block;
        font-size: var(--font-size-sm);
        font-weight: 500;
        color: var(--color-text-secondary);
        margin-bottom: var(--space-2);
    }

    .form-actions {
        display: flex;
        justify-content: flex-end;
        margin-top: var(--space-5);
    }

    .project-list {
        display: flex;
        flex-direction: column;
        gap: var(--space-3);
    }

    .project-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: inherit;
        text-decoration: none;
    }

    .project-name {
        font-size: var(--font-size-lg);
        font-weight: 600;
    }

    .project-desc {
        color: var(--color-text-secondary);
        font-size: var(--font-size-sm);
        margin-top: var(--space-1);
    }

    .project-meta {
        color: var(--color-text-muted);
        font-size: var(--font-size-xs);
        margin-top: var(--space-2);
    }

    .alert {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: var(--space-3) var(--space-4);
        border-radius: var(--radius-sm);
        margin-bottom: var(--space-4);
    }

    .alert-error {
        background: rgba(248, 113, 113, 0.1);
        border: 1px solid rgba(248, 113, 113, 0.3);
        color: var(--color-danger);
    }

    .loading {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--space-4);
        padding: var(--space-12) 0;
        color: var(--color-text-secondary);
    }

    .spinner {
        width: 32px;
        height: 32px;
        border: 3px solid var(--color-border);
        border-top-color: var(--color-accent);
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    .empty-state {
        text-align: center;
        padding: var(--space-12) 0;
    }

    .empty-icon {
        font-size: 3rem;
        margin-bottom: var(--space-4);
    }

    .empty-text {
        font-size: var(--font-size-lg);
        color: var(--color-text-secondary);
    }

    .empty-hint {
        font-size: var(--font-size-sm);
        color: var(--color-text-muted);
        margin-top: var(--space-2);
    }
</style>
