<template>
  <div class="particle-container" ref="container">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
const container = ref(null)
let animationId = null
let particles = []
let mouseX = 0
let mouseY = 0

const createParticles = (width, height) => {
  particles = []
  const particleCount = Math.floor((width * height) / 8000)
  
  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      radius: Math.random() * 2 + 1,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      opacity: Math.random() * 0.5 + 0.2,
      color: getRandomColor()
    })
  }
}

const getRandomColor = () => {
  const colors = [
    'rgba(100, 200, 255, ',  
    'rgba(150, 100, 255, ',  
    'rgba(255, 150, 200, ',  
    'rgba(100, 255, 200, '   
  ]
  return colors[Math.floor(Math.random() * colors.length)]
}

const drawParticles = (ctx, width, height) => {
  ctx.clearRect(0, 0, width, height)
  
  particles.forEach((particle, index) => {
    ctx.beginPath()
    ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2)
    ctx.fillStyle = particle.color + particle.opacity + ')'
    ctx.fill()
    
    particle.x += particle.vx
    particle.y += particle.vy
    
    if (particle.x < 0 || particle.x > width) particle.vx *= -1
    if (particle.y < 0 || particle.y > height) particle.vy *= -1
    
    for (let j = index + 1; j < particles.length; j++) {
      const other = particles[j]
      const dx = particle.x - other.x
      const dy = particle.y - other.y
      const distance = Math.sqrt(dx * dx + dy * dy)
      
      if (distance < 100) {
        ctx.beginPath()
        ctx.moveTo(particle.x, particle.y)
        ctx.lineTo(other.x, other.y)
        ctx.strokeStyle = `rgba(150, 200, 255, ${0.1 * (1 - distance / 100)})`
        ctx.lineWidth = 0.5
        ctx.stroke()
      }
    }
  })
}

const animate = () => {
  const ctx = canvas.value.getContext('2d')
  const width = canvas.value.width
  const height = canvas.value.height
  
  drawParticles(ctx, width, height)
  animationId = requestAnimationFrame(animate)
}

const resizeCanvas = () => {
  if (container.value && canvas.value) {
    canvas.value.width = container.value.offsetWidth
    canvas.value.height = container.value.offsetHeight
    createParticles(canvas.value.width, canvas.value.height)
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
.particle-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
}

canvas {
  display: block;
}
</style>
