<template>
  <div class="star-field" ref="starField">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
const starField = ref(null)
let animationId = null
let stars = []
let mouseX = 0
let mouseY = 0

const createStars = (width, height) => {
  stars = []
  const starCount = Math.floor((width * height) / 3000)
  
  for (let i = 0; i < starCount; i++) {
    stars.push({
      x: Math.random() * width,
      y: Math.random() * height,
      radius: Math.random() * 1.5 + 0.5,
      opacity: Math.random() * 0.8 + 0.2,
      speed: Math.random() * 0.5 + 0.1,
      twinkle: Math.random() * Math.PI * 2
    })
  }
}

const drawStars = (ctx, width, height) => {
  ctx.clearRect(0, 0, width, height)
  
  stars.forEach(star => {
    const twinkleOpacity = star.opacity * (0.5 + 0.5 * Math.sin(star.twinkle))
    
    ctx.beginPath()
    ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2)
    ctx.fillStyle = `rgba(255, 255, 255, ${twinkleOpacity})`
    ctx.fill()
    
    star.twinkle += 0.02
    star.y += star.speed
    
    if (star.y > height) {
      star.y = 0
      star.x = Math.random() * width
    }
  })
}

const animate = () => {
  const ctx = canvas.value.getContext('2d')
  const width = canvas.value.width
  const height = canvas.value.height
  
  drawStars(ctx, width, height)
  animationId = requestAnimationFrame(animate)
}

const resizeCanvas = () => {
  if (starField.value && canvas.value) {
    canvas.value.width = starField.value.offsetWidth
    canvas.value.height = starField.value.offsetHeight
    createStars(canvas.value.width, canvas.value.height)
  }
}

onMounted(() => {
  resizeCanvas()
  window.addEventListener('resize', resizeCanvas)
  animate()
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeCanvas)
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
})
</script>

<style scoped>
.star-field {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: linear-gradient(to bottom, #0a0a1a 0%, #1a1a3a 50%, #0d0d2b 100%);
}

canvas {
  display: block;
}
</style>
