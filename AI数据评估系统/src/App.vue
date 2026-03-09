<template>
  <div class="app-container">
    <AIChat />
  </div>
</template>

<script setup>
import AIChat from '../AI.vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: #eaeaea;
}

.app-container {
  min-height: 100vh;
}
</style>