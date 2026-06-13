<template>
  <div class="content-panel content-panel-padded blog-panel">
    <div class="panel-intro flex align-items-start justify-content-between gap-3 flex-wrap">
      <div>
        <h2 class="section-title">Blog posts</h2>
        <p class="section-copy">Create, edit, and remove articles published on the public site.</p>
      </div>
      <Button label="New post" icon="pi pi-plus" size="small" @click="openCreateDialog" />
    </div>

    <DataTable
      class="blog-table mt-4"
      :value="posts"
      :loading="loading"
      striped-rows
      paginator
      :rows="10"
      empty-message="No blog posts yet."
    >
      <Column field="title" header="Title" sortable style="min-width: 14rem">
        <template #body="{ data }">
          <div class="cell-stack">
            <span class="cell-primary">{{ data.title }}</span>
            <span class="cell-secondary">/blog/{{ data.slug }}</span>
          </div>
        </template>
      </Column>
      <Column field="category" header="Category" sortable style="min-width: 8rem" />
      <Column field="date" header="Date" sortable style="min-width: 7rem" />
      <Column header="Featured" style="min-width: 6rem">
        <template #body="{ data }">
          <Tag :value="data.featured ? 'Yes' : 'No'" :severity="data.featured ? 'success' : 'secondary'" />
        </template>
      </Column>
      <Column headerClass="actions-col" bodyClass="actions-col" style="min-width: 7rem">
        <template #header>
          <span class="actions-header">Actions</span>
        </template>
        <template #body="{ data }">
          <div class="actions-cell flex gap-1">
            <Button
              v-tooltip="tooltip('Edit post')"
              icon="pi pi-pencil"
              text
              rounded
              size="small"
              @click="openEditDialog(data)"
            />
            <Button
              v-tooltip="tooltip('Delete post')"
              icon="pi pi-trash"
              text
              rounded
              size="small"
              severity="danger"
              @click="openDeleteDialog(data)"
            />
          </div>
        </template>
      </Column>
    </DataTable>

    <Dialog
      v-model:visible="editorVisible"
      :header="editorMode === 'create' ? 'New blog post' : 'Edit blog post'"
      modal
      :style="{ width: 'min(48rem, 96vw)' }"
      :draggable="false"
    >
      <div class="editor-form flex flex-column gap-3">
        <div class="assist-panel">
          <div class="assist-header flex align-items-center justify-content-between gap-2 flex-wrap">
            <div>
              <h3 class="assist-title">AI assistant</h3>
              <p class="assist-copy">Paste your draft below and generate title, slug, excerpt, tags, and more.</p>
            </div>
            <Button
              label="Generate from draft"
              icon="pi pi-sparkles"
              size="small"
              :loading="assisting"
              :disabled="!aiDraft.trim()"
              @click="runAssist"
            />
          </div>
          <Textarea
            v-model="aiDraft"
            rows="5"
            class="w-full assist-draft"
            placeholder="Paste article draft (markdown or plain text)…"
          />
        </div>

        <div class="field-grid">
          <div class="field-block">
            <label for="postTitle" class="field-label">Title *</label>
            <InputText id="postTitle" v-model="form.title" class="w-full" />
          </div>
          <div class="field-block">
            <label for="postSlug" class="field-label">Slug</label>
            <InputText id="postSlug" v-model="form.slug" class="w-full" placeholder="auto-from-title" />
          </div>
        </div>

        <div class="field-block">
          <label for="postExcerpt" class="field-label">Excerpt</label>
          <Textarea id="postExcerpt" v-model="form.excerpt" rows="2" class="w-full" auto-resize />
        </div>

        <div class="field-block">
          <label for="postContent" class="field-label">Content (Markdown) *</label>
          <Textarea id="postContent" v-model="form.content" rows="14" class="w-full content-area" />
        </div>

        <div class="field-grid">
          <div class="field-block">
            <label for="postCategory" class="field-label">Category *</label>
            <Select
              id="postCategory"
              v-model="form.category"
              :options="categories"
              editable
              class="w-full"
            />
          </div>
          <div class="field-block">
            <label for="postTags" class="field-label">Tags</label>
            <InputText
              id="postTags"
              v-model="tagsInput"
              class="w-full"
              placeholder="Comma-separated"
            />
          </div>
        </div>

        <div class="field-grid">
          <div class="field-block">
            <label for="postAuthor" class="field-label">Author *</label>
            <InputText id="postAuthor" v-model="form.author" class="w-full" />
          </div>
          <div class="field-block">
            <label for="postAuthorRole" class="field-label">Author role *</label>
            <InputText id="postAuthorRole" v-model="form.author_role" class="w-full" />
          </div>
        </div>

        <div class="field-grid">
          <div class="field-block">
            <label for="postDate" class="field-label">Date</label>
            <InputText id="postDate" v-model="form.date" class="w-full" placeholder="YYYY-MM-DD" />
          </div>
          <div class="field-block">
            <label for="postReadTime" class="field-label">Read time (minutes)</label>
            <InputNumber id="postReadTime" v-model="form.read_time" :min="1" :max="120" class="w-full" />
          </div>
        </div>

        <div class="field-block">
          <span class="field-label">Cover color</span>
          <div class="color-palette" role="listbox" aria-label="Cover color">
            <button
              v-for="color in coverColors"
              :key="color.value"
              type="button"
              class="color-swatch"
              :class="{ selected: form.cover_color === color.value, suggested: color.value === suggestedCoverColor }"
              :style="{ backgroundColor: color.value }"
              :title="`${color.label} (${color.value})`"
              :aria-label="color.label"
              :aria-selected="form.cover_color === color.value"
              @click="form.cover_color = color.value"
            />
          </div>
          <small v-if="suggestedCoverColor" class="field-hint">
            AI suggested {{ suggestedCoverColor }} — click a swatch to change.
          </small>
        </div>
        <div class="field-block flex align-items-end">
          <div class="flex align-items-center gap-2">
            <Checkbox v-model="form.featured" input-id="postFeatured" binary />
            <label for="postFeatured" class="checkbox-label">Featured on home page</label>
          </div>
        </div>
      </div>

      <template #footer>
        <Button label="Cancel" text @click="editorVisible = false" />
        <Button
          :label="editorMode === 'create' ? 'Create post' : 'Save changes'"
          icon="pi pi-check"
          :loading="saving"
          @click="submitEditor"
        />
      </template>
    </Dialog>

    <Dialog
      v-model:visible="deleteVisible"
      header="Delete blog post"
      modal
      :style="{ width: 'min(28rem, 92vw)' }"
      :draggable="false"
    >
      <div v-if="selectedPost" class="flex flex-column gap-3">
        <Message severity="warn" :closable="false">
          This permanently removes the post from the public site.
        </Message>
        <p class="dialog-copy m-0">
          Delete <strong>{{ selectedPost.title }}</strong>?
        </p>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="deleteVisible = false" />
        <Button
          label="Delete post"
          icon="pi pi-trash"
          severity="danger"
          :loading="saving"
          @click="submitDelete"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import InputNumber from 'primevue/inputnumber'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import Textarea from 'primevue/textarea'
import {
  assistBlogPost,
  createBlogPost,
  deleteBlogPost,
  listBlogPosts,
  updateBlogPost,
} from '@/api/client'

const toast = useToast()

const posts = ref([])
const loading = ref(false)
const saving = ref(false)
const assisting = ref(false)
const editorVisible = ref(false)
const deleteVisible = ref(false)
const editorMode = ref('create')
const selectedPost = ref(null)
const tagsInput = ref('')
const aiDraft = ref('')
const suggestedCoverColor = ref('')

const categories = [
  'WAF & Security',
  'Zero-Trust',
  'AI & Automation',
  'Cloud Security',
  'Security',
]

const coverColors = [
  { value: '#007BA7', label: 'Cerulean' },
  { value: '#00A8E0', label: 'Sky' },
  { value: '#005F7F', label: 'Deep teal' },
  { value: '#38383D', label: 'Graphite' },
  { value: '#4DB8E0', label: 'Light blue' },
]

const defaultForm = () => ({
  title: '',
  slug: '',
  excerpt: '',
  content: '# Title\n\n',
  category: 'WAF & Security',
  author: 'Juan Pablo Otalvaro',
  author_role: 'Principal Cloud & Security Architect',
  date: new Date().toISOString().slice(0, 10),
  read_time: null,
  featured: false,
  cover_color: '#007BA7',
})

const form = ref(defaultForm())

function tooltip(text) {
  return { value: text, showDelay: 400 }
}

function parseTags(value) {
  return value
    .split(',')
    .map((tag) => tag.trim())
    .filter(Boolean)
}

function buildPayload() {
  return {
    title: form.value.title.trim(),
    slug: form.value.slug.trim(),
    excerpt: form.value.excerpt.trim(),
    content: form.value.content.trim(),
    category: form.value.category.trim(),
    tags: parseTags(tagsInput.value),
    author: form.value.author.trim(),
    author_role: form.value.author_role.trim(),
    date: form.value.date.trim(),
    read_time: form.value.read_time,
    featured: form.value.featured,
    cover_color: form.value.cover_color,
  }
}

async function loadPosts() {
  loading.value = true
  try {
    posts.value = await listBlogPosts()
  } catch (error) {
    const detail =
      error.message === 'Session expired — sign in again'
        ? 'Sign out and sign in again to refresh your session.'
        : error.message
    toast.add({
      severity: 'error',
      summary: 'Failed to load blog posts',
      detail,
      life: 7000,
    })
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  editorMode.value = 'create'
  selectedPost.value = null
  form.value = defaultForm()
  tagsInput.value = ''
  aiDraft.value = ''
  suggestedCoverColor.value = ''
  editorVisible.value = true
}

function openEditDialog(post) {
  editorMode.value = 'edit'
  selectedPost.value = post
  form.value = {
    title: post.title,
    slug: post.slug,
    excerpt: post.excerpt,
    content: post.content,
    category: post.category,
    author: post.author,
    author_role: post.author_role,
    date: post.date,
    read_time: post.read_time,
    featured: post.featured,
    cover_color: post.cover_color,
  }
  tagsInput.value = (post.tags || []).join(', ')
  aiDraft.value = post.content
  suggestedCoverColor.value = ''
  editorVisible.value = true
}

async function runAssist() {
  const draft = aiDraft.value.trim()
  if (draft.length < 50) {
    toast.add({
      severity: 'warn',
      summary: 'Draft too short',
      detail: 'Paste at least 50 characters for the assistant to work with.',
      life: 4000,
    })
    return
  }

  assisting.value = true
  try {
    const result = await assistBlogPost(draft)
    form.value.title = result.title
    form.value.slug = result.slug
    form.value.excerpt = result.excerpt
    form.value.content = result.content
    form.value.category = result.category
    form.value.read_time = result.read_time
    form.value.cover_color = result.cover_color
    suggestedCoverColor.value = result.cover_color
    tagsInput.value = (result.tags || []).join(', ')
    toast.add({ severity: 'success', summary: 'Draft analyzed', life: 3000 })
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Assistant failed',
      detail: error.message,
      life: 6000,
    })
  } finally {
    assisting.value = false
  }
}

function openDeleteDialog(post) {
  selectedPost.value = post
  deleteVisible.value = true
}

async function submitEditor() {
  if (!form.value.title.trim() || !form.value.content.trim()) {
    toast.add({
      severity: 'warn',
      summary: 'Missing required fields',
      detail: 'Title and content are required.',
      life: 4000,
    })
    return
  }

  saving.value = true
  try {
    const payload = buildPayload()
    if (editorMode.value === 'create') {
      await createBlogPost(payload)
      toast.add({ severity: 'success', summary: 'Blog post created', life: 3000 })
    } else {
      await updateBlogPost(selectedPost.value.id, payload)
      toast.add({ severity: 'success', summary: 'Blog post updated', life: 3000 })
    }
    editorVisible.value = false
    await loadPosts()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Save failed',
      detail: error.message,
      life: 5000,
    })
  } finally {
    saving.value = false
  }
}

async function submitDelete() {
  if (!selectedPost.value) return
  saving.value = true
  try {
    await deleteBlogPost(selectedPost.value.id)
    toast.add({ severity: 'success', summary: 'Blog post deleted', life: 3000 })
    deleteVisible.value = false
    await loadPosts()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Delete failed',
      detail: error.message,
      life: 5000,
    })
  } finally {
    saving.value = false
  }
}

onMounted(loadPosts)
</script>

<style scoped>
.blog-table :deep(.p-datatable-table) {
  min-width: 40rem;
}

.cell-stack {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  line-height: 1.35;
}

.cell-primary {
  font-size: 0.88rem;
  font-weight: 600;
}

.cell-secondary {
  font-size: 0.78rem;
  color: var(--p-text-muted-color);
}

.field-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.field-block {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.field-label {
  font-size: 0.82rem;
  font-weight: 600;
}

.checkbox-label {
  font-size: 0.88rem;
  cursor: pointer;
}

.dialog-copy {
  color: var(--p-text-muted-color);
  font-size: 0.92rem;
  line-height: 1.5;
}

.content-area :deep(textarea) {
  font-family: Consolas, 'Courier New', monospace;
  font-size: 0.85rem;
}

.actions-col {
  white-space: nowrap;
}

.assist-panel {
  padding: 0.85rem 1rem;
  border-radius: 0.65rem;
  border: 1px dashed var(--p-content-border-color);
  background: color-mix(in srgb, var(--p-primary-color) 4%, var(--p-surface-0));
}

.assist-title {
  margin: 0;
  font-size: 0.92rem;
  font-weight: 600;
}

.assist-copy {
  margin: 0.2rem 0 0;
  font-size: 0.78rem;
  color: var(--p-text-muted-color);
}

.assist-draft :deep(textarea) {
  font-family: Consolas, 'Courier New', monospace;
  font-size: 0.85rem;
}

.color-palette {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
}

.color-swatch {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 0.45rem;
  border: 2px solid transparent;
  cursor: pointer;
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--p-surface-900) 12%, transparent);
  transition: transform 0.12s ease, border-color 0.12s ease;
}

.color-swatch:hover {
  transform: scale(1.06);
}

.color-swatch.selected {
  border-color: var(--p-surface-900);
  box-shadow: 0 0 0 2px var(--p-surface-0), 0 0 0 4px var(--p-primary-color);
}

.color-swatch.suggested:not(.selected) {
  border-color: var(--p-primary-color);
}

.field-hint {
  font-size: 0.78rem;
  color: var(--p-text-muted-color);
}

@media (max-width: 720px) {
  .field-grid {
    grid-template-columns: 1fr;
  }
}
</style>
