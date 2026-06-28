<template>
  <div
    ref="mountRef"
    class="magic-rings-container"
    :style="containerStyle"
  />
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import * as THREE from 'three'
import './MagicRings.css'

const vertexShader = `
void main() {
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
`

const fragmentShader = `
precision highp float;

uniform float uTime, uAttenuation, uLineThickness;
uniform float uBaseRadius, uRadiusStep, uScaleRate;
uniform float uOpacity, uNoiseAmount, uRotation, uRingGap;
uniform float uFadeIn, uFadeOut;
uniform float uMouseInfluence, uHoverAmount, uHoverScale, uParallax, uBurst;
uniform vec2 uResolution, uMouse;
uniform vec3 uColor, uColorTwo;
uniform int uRingCount;

const float HP = 1.5707963;
const float CYCLE = 3.45;

float fade(float t) {
  return t < uFadeIn ? smoothstep(0.0, uFadeIn, t) : 1.0 - smoothstep(uFadeOut, CYCLE - 0.2, t);
}

float ring(vec2 p, float ri, float cut, float t0, float px) {
  float t = mod(uTime + t0, CYCLE);
  float r = ri + t / CYCLE * uScaleRate;
  float d = abs(length(p) - r);
  float a = atan(abs(p.y), abs(p.x)) / HP;
  float th = max(1.0 - a, 0.5) * px * uLineThickness;
  float h = (1.0 - smoothstep(th, th * 1.5, d)) + 1.0;
  d += pow(cut * a, 3.0) * r;
  return h * exp(-uAttenuation * d) * fade(t);
}

void main() {
  float px = 1.0 / min(uResolution.x, uResolution.y);
  vec2 p = (gl_FragCoord.xy - 0.5 * uResolution.xy) * px;
  float cr = cos(uRotation), sr = sin(uRotation);
  p = mat2(cr, -sr, sr, cr) * p;
  p -= uMouse * uMouseInfluence;
  float sc = mix(1.0, uHoverScale, uHoverAmount) + uBurst * 0.3;
  p /= sc;
  vec3 c = vec3(0.0);
  float rcf = max(float(uRingCount) - 1.0, 1.0);
  for (int i = 0; i < 10; i++) {
    if (i >= uRingCount) break;
    float fi = float(i);
    vec2 pr = p - fi * uParallax * uMouse;
    vec3 rc = mix(uColor, uColorTwo, fi / rcf);
    c = mix(c, rc, vec3(ring(pr, uBaseRadius + fi * uRadiusStep, pow(uRingGap, fi), i == 0 ? 0.0 : 2.95 * fi, px)));
  }
  c *= 1.0 + uBurst * 2.0;
  float n = fract(sin(dot(gl_FragCoord.xy + uTime * 100.0, vec2(12.9898, 78.233))) * 43758.5453);
  c += (n - 0.5) * uNoiseAmount;
  gl_FragColor = vec4(c, max(c.r, max(c.g, c.b)) * uOpacity);
}
`

const props = defineProps({
  color: { type: String, default: '#00A8E0' },
  colorTwo: { type: String, default: '#007BA7' },
  ringCount: { type: Number, default: 6 },
  speed: { type: Number, default: 1 },
  attenuation: { type: Number, default: 10 },
  lineThickness: { type: Number, default: 2 },
  baseRadius: { type: Number, default: 0.35 },
  radiusStep: { type: Number, default: 0.1 },
  scaleRate: { type: Number, default: 0.1 },
  opacity: { type: Number, default: 1 },
  blur: { type: Number, default: 0 },
  noiseAmount: { type: Number, default: 0.1 },
  rotation: { type: Number, default: 0 },
  ringGap: { type: Number, default: 1.5 },
  fadeIn: { type: Number, default: 0.7 },
  fadeOut: { type: Number, default: 0.5 },
  followMouse: { type: Boolean, default: false },
  mouseInfluence: { type: Number, default: 0.2 },
  hoverScale: { type: Number, default: 1.2 },
  parallax: { type: Number, default: 0.05 },
  clickBurst: { type: Boolean, default: false },
})

const mountRef = ref(null)

const containerStyle = computed(() =>
  props.blur > 0 ? { filter: `blur(${props.blur}px)` } : undefined,
)

let renderer = null
let material = null
let frameId = 0
let resizeObserver = null
let mouse = [0, 0]
let smoothMouse = [0, 0]
let hoverAmount = 0
let isHovered = false
let burst = 0
let prefersReducedMotion = false

function resize() {
  const mount = mountRef.value
  if (!mount || !renderer || !material) return

  const w = mount.clientWidth
  const h = mount.clientHeight
  if (!w || !h) return

  const dpr = Math.min(window.devicePixelRatio || 1, 2)
  renderer.setSize(w, h)
  renderer.setPixelRatio(dpr)
  material.uniforms.uResolution.value.set(w * dpr, h * dpr)
}

function syncUniforms(time) {
  if (!material) return

  smoothMouse[0] += (mouse[0] - smoothMouse[0]) * 0.08
  smoothMouse[1] += (mouse[1] - smoothMouse[1]) * 0.08
  hoverAmount += ((isHovered ? 1 : 0) - hoverAmount) * 0.08
  burst *= 0.95
  if (burst < 0.001) burst = 0

  material.uniforms.uTime.value = prefersReducedMotion ? 0 : time * 0.001 * props.speed
  material.uniforms.uAttenuation.value = props.attenuation
  material.uniforms.uColor.value.set(props.color)
  material.uniforms.uColorTwo.value.set(props.colorTwo)
  material.uniforms.uLineThickness.value = props.lineThickness
  material.uniforms.uBaseRadius.value = props.baseRadius
  material.uniforms.uRadiusStep.value = props.radiusStep
  material.uniforms.uScaleRate.value = props.scaleRate
  material.uniforms.uRingCount.value = props.ringCount
  material.uniforms.uOpacity.value = props.opacity
  material.uniforms.uNoiseAmount.value = props.noiseAmount
  material.uniforms.uRotation.value = (props.rotation * Math.PI) / 180
  material.uniforms.uRingGap.value = props.ringGap
  material.uniforms.uFadeIn.value = props.fadeIn
  material.uniforms.uFadeOut.value = props.fadeOut
  material.uniforms.uMouse.value.set(smoothMouse[0], smoothMouse[1])
  material.uniforms.uMouseInfluence.value = props.followMouse ? props.mouseInfluence : 0
  material.uniforms.uHoverAmount.value = hoverAmount
  material.uniforms.uHoverScale.value = props.hoverScale
  material.uniforms.uParallax.value = props.parallax
  material.uniforms.uBurst.value = props.clickBurst ? burst : 0
}

function animate(t) {
  frameId = requestAnimationFrame(animate)
  syncUniforms(t)
  renderer?.render(renderer.scene, renderer.camera)
}

function onMouseMove(e) {
  const mount = mountRef.value
  if (!mount) return
  const rect = mount.getBoundingClientRect()
  mouse[0] = (e.clientX - rect.left) / rect.width - 0.5
  mouse[1] = -((e.clientY - rect.top) / rect.height - 0.5)
}

function onMouseEnter() {
  isHovered = true
}

function onMouseLeave() {
  isHovered = false
  mouse[0] = 0
  mouse[1] = 0
}

function onClick() {
  burst = 1
}

function initMagicRings() {
  const mount = mountRef.value
  if (!mount) return

  try {
    renderer = new THREE.WebGLRenderer({ alpha: true })
  } catch {
    return
  }

  if (!renderer.capabilities.isWebGL2) {
    renderer.dispose()
    renderer = null
    return
  }

  renderer.setClearColor(0x000000, 0)
  mount.appendChild(renderer.domElement)

  const scene = new THREE.Scene()
  const camera = new THREE.OrthographicCamera(-0.5, 0.5, 0.5, -0.5, 0.1, 10)
  camera.position.z = 1
  renderer.scene = scene
  renderer.camera = camera

  const uniforms = {
    uTime: { value: 0 },
    uAttenuation: { value: props.attenuation },
    uResolution: { value: new THREE.Vector2() },
    uColor: { value: new THREE.Color(props.color) },
    uColorTwo: { value: new THREE.Color(props.colorTwo) },
    uLineThickness: { value: props.lineThickness },
    uBaseRadius: { value: props.baseRadius },
    uRadiusStep: { value: props.radiusStep },
    uScaleRate: { value: props.scaleRate },
    uRingCount: { value: props.ringCount },
    uOpacity: { value: props.opacity },
    uNoiseAmount: { value: props.noiseAmount },
    uRotation: { value: 0 },
    uRingGap: { value: props.ringGap },
    uFadeIn: { value: props.fadeIn },
    uFadeOut: { value: props.fadeOut },
    uMouse: { value: new THREE.Vector2() },
    uMouseInfluence: { value: 0 },
    uHoverAmount: { value: 0 },
    uHoverScale: { value: props.hoverScale },
    uParallax: { value: props.parallax },
    uBurst: { value: 0 },
  }

  material = new THREE.ShaderMaterial({
    vertexShader,
    fragmentShader,
    uniforms,
    transparent: true,
  })

  scene.add(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), material))

  resizeObserver = new ResizeObserver(resize)
  resizeObserver.observe(mount)
  window.addEventListener('resize', resize)
  mount.addEventListener('mousemove', onMouseMove)
  mount.addEventListener('mouseenter', onMouseEnter)
  mount.addEventListener('mouseleave', onMouseLeave)
  mount.addEventListener('click', onClick)

  resize()
  frameId = requestAnimationFrame(animate)
}

function destroyMagicRings() {
  cancelAnimationFrame(frameId)
  frameId = 0

  window.removeEventListener('resize', resize)
  resizeObserver?.disconnect()
  resizeObserver = null

  const mount = mountRef.value
  if (mount) {
    mount.removeEventListener('mousemove', onMouseMove)
    mount.removeEventListener('mouseenter', onMouseEnter)
    mount.removeEventListener('mouseleave', onMouseLeave)
    mount.removeEventListener('click', onClick)
    if (renderer?.domElement?.parentNode === mount) {
      mount.removeChild(renderer.domElement)
    }
  }

  material?.dispose()
  renderer?.dispose()

  material = null
  renderer = null
}

onMounted(() => {
  prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  initMagicRings()
})

onBeforeUnmount(() => {
  destroyMagicRings()
})
</script>
