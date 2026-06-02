<template>
  <div class="blog-post-page">
    <div v-if="loading" class="loading-screen">
      <i class="pi pi-spin pi-spinner"></i>
    </div>
    <div v-else-if="post">
      <!-- Hero -->
      <section class="post-hero" :style="{ background: post.cover_color }">
        <div class="post-hero-overlay"></div>
        <div class="container post-hero-content">
          <span class="tag tag-teal">{{ post.category }}</span>
          <h1>{{ post.title }}</h1>
          <div class="post-meta">
            <div class="post-author">
              <div class="author-avatar">JP</div>
              <div>
                <span class="author-name">{{ post.author }}</span>
                <span class="author-role">{{ post.author_role }}</span>
              </div>
            </div>
            <div class="post-info">
              <span><i class="pi pi-calendar"></i> {{ formatDate(post.date) }}</span>
              <span><i class="pi pi-clock"></i> {{ post.read_time }} min read</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Content -->
      <section class="post-body-section">
        <div class="container post-layout">
          <article class="post-content">
            <div class="post-tags">
              <span v-for="tag in post.tags" :key="tag" class="tag">{{ tag }}</span>
            </div>
            <div class="markdown-body" v-html="renderedContent"></div>
            <div class="post-footer">
              <RouterLink to="/blog" class="btn btn-outline">
                <i class="pi pi-arrow-left"></i> Back to Blog
              </RouterLink>
              <RouterLink to="/contact" class="btn btn-primary">
                <i class="pi pi-send"></i> Discuss with Us
              </RouterLink>
            </div>
          </article>

          <!-- Sidebar -->
          <aside class="post-sidebar">
            <div class="sidebar-card">
              <h4>About the Author</h4>
              <div class="sidebar-author">
                <div class="author-avatar-lg">JP</div>
                <div>
                  <strong>{{ post.author }}</strong>
                  <span>{{ post.author_role }}</span>
                </div>
              </div>
              <p>Principal Cloud &amp; Security Architect with 15+ years across 54+ countries. Citrix SME. AWS Certified.</p>
              <RouterLink to="/about" class="btn btn-outline sidebar-btn">
                Full Profile <i class="pi pi-arrow-right"></i>
              </RouterLink>
            </div>
            <div class="sidebar-card">
              <h4>Need Help With This?</h4>
              <p>We implement everything we write about. Let's talk about your specific environment.</p>
              <RouterLink to="/contact" class="btn btn-primary sidebar-btn">
                <i class="pi pi-send"></i> Get a Consultation
              </RouterLink>
            </div>
            <div class="sidebar-card" v-if="relatedPosts.length">
              <h4>Related Posts</h4>
              <div class="related-posts">
                <div
                  v-for="rp in relatedPosts"
                  :key="rp.id"
                  class="related-post"
                  @click="$router.push(`/blog/${rp.slug}`)"
                >
                  <span class="tag tag-teal" style="font-size:0.7rem">{{ rp.category }}</span>
                  <p>{{ rp.title }}</p>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </section>
    </div>
    <div v-else class="not-found">
      <h2>Post not found.</h2>
      <RouterLink to="/blog" class="btn btn-outline">Back to Blog</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const post = ref(null)
const allPosts = ref([])
const loading = ref(true)

const formatDate = (d) =>
  new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })

const renderedContent = computed(() => post.value ? renderMarkdown(post.value.content) : '')

const relatedPosts = computed(() => {
  if (!post.value) return []
  return allPosts.value
    .filter(p => p.id !== post.value.id && (
      p.category === post.value.category ||
      p.tags.some(t => post.value.tags.includes(t))
    ))
    .slice(0, 3)
})

const fetchPost = async (slug) => {
  loading.value = true
  try {
    const [postRes, allRes] = await Promise.all([
      axios.get(`/api/blog/${slug}`),
      axios.get('/api/blog'),
    ])
    post.value = postRes.data
    allPosts.value = allRes.data
    document.title = `${post.value.title} — Nexxus Tech Blog`
  } catch {
    post.value = null
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchPost(route.params.slug))
watch(() => route.params.slug, (slug) => fetchPost(slug))
</script>

<style scoped>
.loading-screen, .not-found {
  min-height: 60vh; display: flex; align-items: center; justify-content: center;
  flex-direction: column; gap: 24px; color: var(--nt-text-muted);
}
.loading-screen .pi { font-size: 2rem; }

.post-hero {
  padding: 140px 0 60px;
  position: relative;
  overflow: hidden;
}
.post-hero-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0.6) 100%);
}
.post-hero-content { position: relative; z-index: 1; max-width: 800px; }
.post-hero-content h1 { font-size: clamp(1.8rem, 4vw, 3rem); color: white; margin: 16px 0 24px; }
.post-meta { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }
.post-author { display: flex; align-items: center; gap: 12px; }
.author-avatar {
  width: 40px; height: 40px; border-radius: 50%;
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-secondary));
  display: flex; align-items: center; justify-content: center;
  font-size: 0.8rem; font-weight: 800; color: white; font-family: var(--font-heading);
}
.author-name { display: block; font-size: 0.85rem; font-weight: 600; color: white; }
.author-role { display: block; font-size: 0.75rem; color: rgba(255,255,255,0.65); }
.post-info { display: flex; gap: 20px; font-size: 0.82rem; color: rgba(255,255,255,0.7); }
.post-info .pi { margin-right: 5px; }

.post-body-section { padding: 60px 0 80px; }
.post-layout { display: grid; grid-template-columns: 1fr 320px; gap: 56px; align-items: start; }
.post-content { min-width: 0; }
.post-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 32px; }

.markdown-body {
  font-size: 1rem;
  line-height: 1.8;
  color: var(--nt-text-light);
}
.markdown-body :deep(h1), .markdown-body :deep(h2), .markdown-body :deep(h3) {
  color: var(--nt-white);
  margin: 32px 0 12px;
  font-family: var(--font-heading);
}
.markdown-body :deep(h1) { font-size: 2rem; }
.markdown-body :deep(h2) { font-size: 1.5rem; }
.markdown-body :deep(h3) { font-size: 1.2rem; }
.markdown-body :deep(p) { margin: 0 0 16px; }
.markdown-body :deep(ul) { padding-left: 24px; margin: 12px 0 20px; }
.markdown-body :deep(li) { margin: 6px 0; color: var(--nt-text-light); }
.markdown-body :deep(code) {
  background: rgba(91,79,232,0.15);
  border: 1px solid rgba(91,79,232,0.25);
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 0.875em;
  font-family: 'Fira Code', 'Consolas', monospace;
  color: var(--nt-secondary);
}
.markdown-body :deep(pre) {
  background: var(--nt-dark-3);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius);
  padding: 24px;
  overflow-x: auto;
  margin: 24px 0;
}
.markdown-body :deep(pre code) {
  background: none; border: none; padding: 0;
  font-size: 0.875rem; color: var(--nt-text);
}
.markdown-body :deep(a) { color: var(--nt-secondary); }
.markdown-body :deep(strong) { color: var(--nt-white); font-weight: 700; }

.post-footer { display: flex; gap: 16px; margin-top: 48px; padding-top: 32px; border-top: 1px solid var(--nt-border); }

/* Sidebar */
.post-sidebar { display: flex; flex-direction: column; gap: 24px; position: sticky; top: 100px; }
.sidebar-card {
  background: var(--nt-card-bg);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius);
  padding: 24px;
}
.sidebar-card h4 { font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--nt-secondary); margin-bottom: 16px; }
.sidebar-author { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.author-avatar-lg {
  width: 48px; height: 48px; border-radius: 50%;
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-secondary));
  display: flex; align-items: center; justify-content: center;
  font-size: 0.9rem; font-weight: 800; color: white; font-family: var(--font-heading);
  flex-shrink: 0;
}
.sidebar-author strong { display: block; font-size: 0.9rem; color: var(--nt-white); }
.sidebar-author span { font-size: 0.78rem; color: var(--nt-text-muted); }
.sidebar-card p { font-size: 0.85rem; color: var(--nt-text-muted); line-height: 1.6; margin-bottom: 16px; }
.sidebar-btn { width: 100%; justify-content: center; font-size: 0.82rem; padding: 10px; }
.related-posts { display: flex; flex-direction: column; gap: 12px; }
.related-post {
  cursor: pointer;
  padding: 12px;
  background: rgba(255,255,255,0.03);
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.05);
  transition: var(--nt-transition);
}
.related-post:hover { border-color: var(--nt-border); background: rgba(91,79,232,0.08); }
.related-post p { font-size: 0.82rem; color: var(--nt-text-light); margin: 6px 0 0; line-height: 1.4; }

@media (max-width: 1024px) {
  .post-layout { grid-template-columns: 1fr; }
  .post-sidebar { position: static; }
}
@media (max-width: 640px) {
  .post-footer { flex-direction: column; }
  .post-meta { flex-direction: column; }
}
</style>
