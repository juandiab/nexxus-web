<script setup>
import { computed } from 'vue'
import { GOOGLE_APPOINTMENT_SCHEDULE_URL } from '@/config/site.js'

const props = defineProps({
  src: { type: String, default: '' },
  title: { type: String, default: 'Schedule a demo with Nexxus Tech' },
  minHeight: { type: [String, Number], default: 600 },
})

const iframeSrc = computed(() => props.src || GOOGLE_APPOINTMENT_SCHEDULE_URL)

const frameMinHeight = computed(() =>
  typeof props.minHeight === 'number' ? `${props.minHeight}px` : props.minHeight
)
</script>

<template>
  <div class="appointment-scheduler" :style="{ minHeight: frameMinHeight }">
    <iframe
      :src="iframeSrc"
      :title="title"
      class="appointment-scheduler__frame"
      frameborder="0"
      allow="clipboard-write"
      loading="lazy"
    />
  </div>
</template>

<style scoped>
.appointment-scheduler {
  width: 100%;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.appointment-scheduler__frame {
  width: 100%;
  height: 100%;
  min-height: inherit;
  border: 0;
  display: block;
}
</style>
