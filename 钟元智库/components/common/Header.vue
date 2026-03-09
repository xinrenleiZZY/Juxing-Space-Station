<template>
  <nav class="bg-white shadow-md fixed w-full z-50">
    <div class="container mx-auto px-4 py-3">
      <div class="flex justify-between items-center">
        <div class="flex items-center">
          <a href="/" class="text-2xl font-bold text-primary">
            钟元智库
          </a>
          <span class="ml-2 text-sm text-gray-500">数据知识产权</span>
        </div>
        <div class="hidden md:flex space-x-8">
          <a href="/" class="text-primary font-medium hover:text-secondary transition-colors">首页</a>
          <a href="/services" class="text-gray-600 font-medium hover:text-primary transition-colors">服务中心</a>
          <a href="/about" class="text-gray-600 font-medium hover:text-primary transition-colors">关于我们</a>
          <a href="/news" class="text-gray-600 font-medium hover:text-primary transition-colors">新闻动态</a>
          <a href="/contact" class="text-gray-600 font-medium hover:text-primary transition-colors">联系我们</a>
        </div>
        <div class="md:hidden">
          <button @click="toggleMenu" class="text-gray-600 focus:outline-none">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
      <!-- Mobile menu -->
      <div v-if="menuOpen" class="md:hidden mt-4 pb-4">
        <a href="/" class="block py-2 text-primary font-medium">首页</a>
        <a href="/services" class="block py-2 text-gray-600 font-medium hover:text-primary">服务中心</a>
        <a href="/about" class="block py-2 text-gray-600 font-medium hover:text-primary">关于我们</a>
        <a href="/news" class="block py-2 text-gray-600 font-medium hover:text-primary">新闻动态</a>
        <a href="/contact" class="block py-2 text-gray-600 font-medium hover:text-primary">联系我们</a>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const menuOpen = ref(false)

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}
</script>
