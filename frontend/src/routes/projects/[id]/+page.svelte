<!--
  プロジェクト詳細ページ

  - プロジェクト情報の表示
  - タスク一覧の表示
  - タスク作成フォーム
  - タスクのステータス変更・削除
-->
<script lang="ts">
  import { page } from '$app/stores';
  import {
    getProject,
    getTasks,
    createTask,
    updateTask,
    deleteTask,
  } from '$lib/api/client';
  import type { Project, Task, TaskCreate, TaskStatus } from '$lib/types';

  // --- リアクティブ state ---
  let project = $state<Project | null>(null);
  let tasks = $state<Task[]>([]);
  let loading = $state(true);
  let error = $state<string | null>(null);

  // タスク作成フォーム
  let showTaskForm = $state(false);
  let newTitle = $state('');
  let newTaskDesc = $state('');
  let newPriority = $state(0);
  let creating = $state(false);

  // ページパラメータからプロジェクトIDを取得
  let projectId = $derived($page.params.id);

  // データ読み込み
  async function loadData() {
    loading = true;
    error = null;
    try {
      const [proj, taskRes] = await Promise.all([
        getProject(projectId),
        getTasks(projectId),
      ]);
      project = proj;
      tasks = taskRes.items;
    } catch (e) {
      error = e instanceof Error ? e.message : '読み込みに失敗しました';
    } finally {
      loading = false;
    }
  }

  // タスク作成
  async function handleCreateTask() {
    if (!newTitle.trim()) return;
    creating = true;
    try {
      const data: TaskCreate = {
        title: newTitle.trim(),
        description: newTaskDesc.trim() || null,
        priority: newPriority,
      };
      await createTask(projectId, data);
      newTitle = '';
      newTaskDesc = '';
      newPriority = 0;
      showTaskForm = false;
      await loadData();
    } catch (e) {
      error = e instanceof Error ? e.message : '作成に失敗しました';
    } finally {
      creating = false;
    }
  }

  // ステータス変更
  async function handleStatusChange(taskId: string, newStatus: TaskStatus) {
    try {
      await updateTask(projectId, taskId, { status: newStatus });
      await loadData();
    } catch (e) {
      error = e instanceof Error ? e.message : 'ステータス変更に失敗しました';
    }
  }

  // タスク削除（論理削除）
  async function handleDeleteTask(taskId: string) {
    if (!confirm('このタスクを削除しますか？')) return;
    try {
      await deleteTask(projectId, taskId);
      await loadData();
    } catch (e) {
      error = e instanceof Error ? e.message : '削除に失敗しました';
    }
  }

  // ステータスのラベルマッピング
  function statusLabel(status: TaskStatus): string {
    const labels: Record<TaskStatus, string> = {
      todo: 'TODO',
      in_progress: '進行中',
      done: '完了',
    };
    return labels[status];
  }

  // ステータスのバッジCSSクラス
  function statusBadgeClass(status: TaskStatus): string {
    const classes: Record<TaskStatus, string> = {
      todo: 'badge-todo',
      in_progress: 'badge-in-progress',
      done: 'badge-done',
    };
    return classes[status];
  }

  // 日付フォーマット
  function formatDate(dateStr: string): string {
    return new Date(dateStr).toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  }

  // 初回ロード
  $effect(() => {
    loadData();
  });
</script>

<svelte:head>
  <title>{project?.name ?? '読み込み中...'} | Training-0</title>
</svelte:head>

<div class="container">
  {#if loading}
    <div class="loading">
      <div class="spinner"></div>
      <p>読み込み中...</p>
    </div>
  {:else if error}
    <div class="alert alert-error">
      <span>⚠️ {error}</span>
    </div>
  {:else if project}
    <!-- プロジェクト情報 -->
    <div class="breadcrumb">
      <a href="/">← プロジェクト一覧</a>
    </div>

    <div class="project-header">
      <div>
        <h1 class="page-title">{project.name}</h1>
        {#if project.description}
          <p class="project-desc">{project.description}</p>
        {/if}
        <p class="project-meta">
          作成日: {formatDate(project.created_at)} ・ 更新日: {formatDate(project.updated_at)}
        </p>
      </div>
    </div>

    <!-- タスクセクション -->
    <section class="tasks-section">
      <div class="section-header">
        <h2 class="section-title">タスク ({tasks.length})</h2>
        <button class="btn btn-primary btn-sm" onclick={() => (showTaskForm = !showTaskForm)}>
          {showTaskForm ? '✕ キャンセル' : '＋ タスク追加'}
        </button>
      </div>

      <!-- タスク作成フォーム -->
      {#if showTaskForm}
        <div class="card" style="margin-bottom: var(--space-4);">
          <form onsubmit={(e) => { e.preventDefault(); handleCreateTask(); }}>
            <div class="form-group">
              <label for="task-title" class="label">タイトル *</label>
              <input
                id="task-title"
                class="input"
                type="text"
                bind:value={newTitle}
                placeholder="例：API エンドポイントの実装"
                required
              />
            </div>
            <div class="form-row">
              <div class="form-group" style="flex: 1;">
                <label for="task-desc" class="label">説明（任意）</label>
                <textarea
                  id="task-desc"
                  class="textarea"
                  bind:value={newTaskDesc}
                  placeholder="タスクの詳細..."
                ></textarea>
              </div>
              <div class="form-group" style="width: 120px;">
                <label for="task-priority" class="label">優先度</label>
                <input
                  id="task-priority"
                  class="input"
                  type="number"
                  bind:value={newPriority}
                  min="0"
                />
              </div>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn btn-primary btn-sm" disabled={creating || !newTitle.trim()}>
                {creating ? '追加中...' : 'タスクを追加'}
              </button>
            </div>
          </form>
        </div>
      {/if}

      <!-- タスク一覧 -->
      {#if tasks.length === 0}
        <div class="empty-state">
          <p class="empty-text">タスクがありません</p>
          <p class="empty-hint">「タスク追加」ボタンから新しいタスクを作成しましょう</p>
        </div>
      {:else}
        <div class="task-list">
          {#each tasks as task (task.id)}
            <div class="card task-card" class:task-done={task.status === 'done'}>
              <div class="task-info">
                <div class="task-header">
                  <h3 class="task-title">{task.title}</h3>
                  <span class="badge {statusBadgeClass(task.status)}">{statusLabel(task.status)}</span>
                </div>
                {#if task.description}
                  <p class="task-desc">{task.description}</p>
                {/if}
                <p class="task-meta">
                  優先度: {task.priority} ・ 作成日: {formatDate(task.created_at)}
                </p>
              </div>
              <div class="task-actions">
                <!-- ステータス変更ドロップダウン -->
                <select
                  class="input status-select"
                  value={task.status}
                  onchange={(e) => handleStatusChange(task.id, (e.target as HTMLSelectElement).value as TaskStatus)}
                >
                  <option value="todo">TODO</option>
                  <option value="in_progress">進行中</option>
                  <option value="done">完了</option>
                </select>
                <button
                  class="btn btn-sm btn-danger"
                  onclick={() => handleDeleteTask(task.id)}
                >
                  削除
                </button>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </section>
  {/if}
</div>

<style>
  .breadcrumb {
    margin-bottom: var(--space-6);
  }

  .breadcrumb a {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
  }

  .breadcrumb a:hover {
    color: var(--color-accent);
  }

  .page-title {
    font-size: var(--font-size-3xl);
    font-weight: 700;
    letter-spacing: -0.02em;
  }

  .project-desc {
    color: var(--color-text-secondary);
    margin-top: var(--space-2);
  }

  .project-meta {
    color: var(--color-text-muted);
    font-size: var(--font-size-xs);
    margin-top: var(--space-2);
  }

  .project-header {
    margin-bottom: var(--space-8);
    padding-bottom: var(--space-6);
    border-bottom: 1px solid var(--color-border);
  }

  .tasks-section {
    margin-top: var(--space-4);
  }

  .section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--space-5);
  }

  .section-title {
    font-size: var(--font-size-xl);
    font-weight: 600;
  }

  .task-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  .task-card {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: var(--space-4);
  }

  .task-done {
    opacity: 0.6;
  }

  .task-header {
    display: flex;
    align-items: center;
    gap: var(--space-3);
  }

  .task-title {
    font-size: var(--font-size-base);
    font-weight: 600;
  }

  .task-desc {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
    margin-top: var(--space-1);
  }

  .task-meta {
    color: var(--color-text-muted);
    font-size: var(--font-size-xs);
    margin-top: var(--space-2);
  }

  .task-actions {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    flex-shrink: 0;
  }

  .status-select {
    width: auto;
    padding: var(--space-1) var(--space-3);
    font-size: var(--font-size-xs);
  }

  .form-row {
    display: flex;
    gap: var(--space-4);
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
    to { transform: rotate(360deg); }
  }

  .alert-error {
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-sm);
    background: rgba(248, 113, 113, 0.1);
    border: 1px solid rgba(248, 113, 113, 0.3);
    color: var(--color-danger);
  }

  .empty-state {
    text-align: center;
    padding: var(--space-8) 0;
  }

  .empty-text {
    color: var(--color-text-secondary);
  }

  .empty-hint {
    font-size: var(--font-size-sm);
    color: var(--color-text-muted);
    margin-top: var(--space-2);
  }
</style>
