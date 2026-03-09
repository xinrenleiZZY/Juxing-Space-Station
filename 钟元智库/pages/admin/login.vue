<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-primary mb-2">钟元智库</h1>
        <p class="text-gray-600">后台管理系统</p>
      </div>
      
      <form @submit.prevent="handleSubmit">
        <div class="mb-6">
          <label for="username" class="block text-gray-700 font-medium mb-2">用户名</label>
          <input 
            id="username" 
            type="text" 
            v-model="username"
            class="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="请输入用户名"
            required
          >
        </div>
        
        <div class="mb-6">
          <label for="password" class="block text-gray-700 font-medium mb-2">密码</label>
          <input 
            id="password" 
            type="password" 
            v-model="password"
            class="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="请输入密码"
            required
          >
        </div>
        
        <button 
          type="submit" 
          class="btn-primary w-full"
        >
          登录
        </button>
      </form>
      
      <div class="mt-6 text-center">
        <a href="/" class="text-primary hover:text-secondary transition-colors">
          返回首页
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const username = ref('')
const password = ref('')

const handleSubmit = () => {
  console.log('Login attempt:', { username: username.value, password: password.value })
}
</script>