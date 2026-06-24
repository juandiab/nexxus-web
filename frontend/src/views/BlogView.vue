<template>
  <div class="blog-page">
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <span class="section-label reveal">Knowledge Hub</span>
        <h1 class="reveal reveal-delay-1">Nexxus Tech<br /><span class="gradient-text">Blog & Insights</span></h1>
        <p class="page-hero-subtitle reveal reveal-delay-2">
          Deep dives into WAF, NetScaler, Zero-Trust, and AI-powered security —
          written by practitioners who've deployed these technologies at global scale.
        </p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <!-- Category filter -->
        <div class="filter-bar reveal">
          <button
            v-for="cat in categories"
            :key="cat"
            :class="['filter-btn', { active: activeCategory === cat }]"
            @click="activeCategory = cat"
          >{{ cat }}</button>
        </div>

        <div v-if="loading" class="loading-state">
          <i class="pi pi-spin pi-spinner"></i> Loading posts...
        </div>

        <div v-else-if="filteredPosts.length" class="blog-grid">
          <article
            v-for="(post, i) in filteredPosts"
            :key="post.id"
            :class="`card blog-card reveal reveal-delay-${(i % 3) + 1}`"
            @click="$router.push(`/blog/${post.slug}`)"
          >
            <div class="blog-card-header" :class="coverColorClass(post.cover_color)">
              <div class="blog-card-overlay"></div>
              <span class="tag tag-on-cover">{{ post.category }}</span>
              <div v-if="post.featured" class="featured-badge">
                <i class="pi pi-star-fill"></i> Featured
              </div>
            </div>
            <div class="blog-card-body">
              <h3 class="blog-title">{{ post.title }}</h3>
              <p class="blog-excerpt">{{ post.excerpt }}</p>
              <div class="blog-footer">
                <div class="blog-author">
                  <div class="author-avatar">JP</div>
                  <div>
                    <span class="author-name">{{ post.author }}</span>
                    <span class="post-date">{{ formatDate(post.date) }}</span>
                  </div>
                </div>
                <div class="blog-meta">
                  <span><i class="pi pi-clock"></i> {{ post.read_time }} min</span>
                </div>
              </div>
              <div class="blog-tags">
                <span v-for="tag in post.tags.slice(0,3)" :key="tag" class="tag">{{ tag }}</span>
              </div>
            </div>
          </article>
        </div>

        <div v-else class="empty-state">
          <i class="pi pi-inbox"></i>
          <p>No posts in this category yet. Check back soon!</p>
        </div>
      </div>
    </section>

    <!-- Newsletter CTA -->
    <section class="section section-dark newsletter-section">
      <div class="container">
        <div class="newsletter-box reveal">
          <div class="newsletter-content">
            <span class="section-label">Stay Updated</span>
            <h2>Get Security Insights Delivered</h2>
            <p>Join security professionals receiving our latest WAF configurations, NetScaler tips, and AI automation guides.</p>
          </div>
          <RouterLink to="/contact" class="btn btn-primary">
            <i class="pi pi-envelope"></i> Get in Touch to Subscribe
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { coverColorClass } from '@/utils/coverColor.js'

const posts = ref([])
const loading = ref(true)
const activeCategory = ref('All')

const categories = computed(() => {
  const cats = ['All', ...new Set(posts.value.map(p => p.category))]
  return cats
})

const filteredPosts = computed(() => {
  if (activeCategory.value === 'All') return posts.value
  return posts.value.filter(p => p.category === activeCategory.value)
})

const formatDate = (d) =>
  new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })

onMounted(async () => {
  try {
    const { data } = await axios.get('/api/blog')
    posts.value = data
  } catch {
    posts.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page-hero {
  min-height: 40vh;
  display: flex; align-items: center;
  background: var(--nt-dark);
  padding: 120px 0 60px;
  position: relative; overflow: hidden;
}
.page-hero-bg {
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 50% 70%, rgba(0,168,224,0.1) 0%, transparent 65%);
}
.page-hero-content { position: relative; z-index: 1; }
.page-hero-subtitle { font-size: 1.05rem; color: var(--nt-text-muted); margin-top: 16px; max-width: 560px; line-height: 1.75; }

.filter-bar { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 40px; }
.filter-btn {
  padding: 8px 20px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 100px;
  color: var(--nt-text-muted);
  font-family: var(--font-heading);
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--nt-transition);
}
.filter-btn:hover, .filter-btn.active {
  background: var(--nt-primary);
  border-color: var(--nt-primary);
  color: white;
}

.blog-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}
.blog-card { cursor: pointer; padding: 0; overflow: hidden; }
.blog-card-header {
  height: 140px;
  position: relative;
  display: flex;
  align-items: flex-end;
  padding: 16px;
}
.blog-card-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, transparent 40%, rgba(0,0,0,0.4) 100%);
}
.blog-card-header .tag-on-cover {
  position: relative;
  z-index: 1;
}
.featured-badge {
  position: absolute; top: 12px; right: 12px;
  background: rgba(255,193,7,0.9);
  color: #1a1a1a;
  padding: 3px 10px;
  border-radius: 100px;
  font-size: 0.72rem;
  font-weight: 700;
  font-family: var(--font-heading);
  display: flex; align-items: center; gap: 4px;
}
.blog-card-body { padding: 24px; }
.blog-title { font-size: 1.05rem; font-weight: 700; margin-bottom: 10px; line-height: 1.4; }
.blog-excerpt {
  font-size: 0.875rem; color: var(--nt-text-muted); line-height: 1.6;
  margin-bottom: 20px;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;
}
.blog-footer { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
.blog-author { display: flex; align-items: center; gap: 10px; }
.author-avatar {
  width: 32px; height: 32px;
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-secondary));
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.7rem; font-weight: 800; color: white;
  font-family: var(--font-heading);
}
.author-name { display: block; font-size: 0.8rem; font-weight: 600; color: var(--nt-text-light); }
.post-date { display: block; font-size: 0.72rem; color: var(--nt-text-muted); }
.blog-meta { font-size: 0.78rem; color: var(--nt-text-muted); }
.blog-meta .pi { margin-right: 4px; }
.blog-tags { display: flex; gap: 6px; flex-wrap: wrap; }

.loading-state, .empty-state {
  text-align: center; color: var(--nt-text-muted); padding: 80px 0; font-size: 0.9rem;
}
.empty-state .pi { font-size: 2rem; display: block; margin-bottom: 12px; }

.newsletter-section { background: var(--nt-dark-2); }
.newsletter-box {
  background: var(--nt-dark-3);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius-lg);
  padding: 48px 56px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
}
.newsletter-content h2 { font-size: 1.6rem; margin: 8px 0 12px; }
.newsletter-content p { color: var(--nt-text-muted); font-size: 0.9rem; max-width: 440px; }

@media (max-width: 1024px) { .blog-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) {
  .blog-grid { grid-template-columns: 1fr; }
  .newsletter-box { flex-direction: column; text-align: center; padding: 40px 24px; }
}
</style>
