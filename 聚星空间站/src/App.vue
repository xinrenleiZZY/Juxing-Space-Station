<template>
  <div id="app">
    <StarField />
    <ParticleEffect />
    <GlowEffect />
    <NavBar />
    
    <router-view v-slot="{ Component }">
      <transition name="page" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    
    <InteractivePanel v-if="route.name === 'home'" />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import StarField from './components/StarField.vue'
import ParticleEffect from './components/ParticleEffect.vue'
import GlowEffect from './components/GlowEffect.vue'
import NavBar from './components/NavBar.vue'
import InteractivePanel from './components/InteractivePanel.vue'

const route = useRoute()
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;
}

#app {
  min-height: 100vh;
  position: relative;
}

.page-enter-active,
.page-leave-active {
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.page-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.95);
  filter: blur(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-30px) scale(1.05);
  filter: blur(10px);
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #764ba2 0%, #f093fb 100%);
}
</style>