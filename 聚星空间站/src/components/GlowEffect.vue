<template>
  <div class="glow-container">
    <div class="glow-orb orb-1"></div>
    <div class="glow-orb orb-2"></div>
    <div class="glow-orb orb-3"></div>
    <div class="glow-line line-1"></div>
    <div class="glow-line line-2"></div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.glow-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
  overflow: hidden;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.3;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(100, 150, 255, 0.8) 0%, transparent 70%);
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(150, 100, 255, 0.8) 0%, transparent 70%);
  bottom: -150px;
  right: -150px;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(100, 255, 200, 0.8) 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

.glow-line {
  position: absolute;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(150, 200, 255, 0.5), transparent);
  animation: moveLine 8s ease-in-out infinite;
}

.line-1 {
  width: 60%;
  top: 30%;
  left: -20%;
  animation-delay: 0s;
}

.line-2 {
  width: 50%;
  top: 70%;
  left: 30%;
  animation-delay: -4s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(50px, 30px) scale(1.1);
  }
  50% {
    transform: translate(20px, 60px) scale(0.9);
  }
  75% {
    transform: translate(-30px, 20px) scale(1.05);
  }
}

@keyframes moveLine {
  0% {
    transform: translateX(-100%);
    opacity: 0;
  }
  50% {
    opacity: 0.6;
  }
  100% {
    transform: translateX(200%);
    opacity: 0;
  }
}
</style>
