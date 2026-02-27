<template>
  <div class="nav-wrapper">
    <div class="floating-logo" @click="toggleNavMenu">
      <span class="logo-icon">⚛</span>
      <span class="logo-text">聚星空间站</span>
    </div>

    <nav :class="['navbar', { show: isNavMenuOpen }]">
      <div class="nav-container">
        <div class="nav-menu">
          <router-link 
            v-for="item in navItems" 
            :key="item.path"
            :to="item.path" 
            class="nav-link"
            active-class="active"
            @click="isNavMenuOpen = false"
          >
            <span class="nav-icon">{{ item.icon }}</span>
            <span class="nav-text">{{ item.label }}</span>
          </router-link>
        </div>

        <div class="nav-actions">
          <button class="nav-toggle" @click="toggleNavMenu">
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </div>

      <div :class="['mobile-menu', { open: isMobileMenuOpen }]">
        <router-link 
          v-for="item in navItems" 
          :key="item.path"
          :to="item.path" 
          class="mobile-link"
          @click="closeMenus"
        >
          <span class="mobile-icon">{{ item.icon }}</span>
          <span class="mobile-text">{{ item.label }}</span>
        </router-link>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isNavMenuOpen = ref(false)
const isMobileMenuOpen = ref(false)

const navItems = [
  { path: '/', label: '主页', icon: '🏠' },
  { path: '/intellectual', label: '钟元智库', icon: '📚' },
  { path: '/ia', label: 'IA 分析', icon: '🤖' }
]

const toggleNavMenu = () => {
  isNavMenuOpen.value = !isNavMenuOpen.value
  isMobileMenuOpen.value = false
}

const closeMenus = () => {
  isNavMenuOpen.value = false
  isMobileMenuOpen.value = false
}
</script>

<style scoped>
.nav-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}

.floating-logo {
  position: fixed;
  top: 20px;
  left: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 15px;
  cursor: pointer;
  user-select: none;
  transition: all 0.3s ease;
  z-index: 1001;
}

.floating-logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 1.8rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.3rem;
  font-weight: 700;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 70px;
  z-index: 1000;
  background: rgba(10, 10, 26, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.4s ease;
  opacity: 0;
  visibility: hidden;
  transform: translateX(-100%);
}

.navbar.show {
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70px;
}

.nav-menu {
  display: flex;
  gap: 10px;
  align-items: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  text-decoration: none;
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  font-weight: 500;
  border-radius: 10px;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  color: white;
  background: rgba(255, 255, 255, 0.05);
}

.nav-link.active {
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.nav-icon {
  font-size: 1.2rem;
}

.nav-actions {
  display: flex;
  align-items: center;
}

.nav-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
}

.nav-toggle span {
  width: 25px;
  height: 2px;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.mobile-menu {
  display: none;
  position: absolute;
  top: 70px;
  left: 0;
  width: 100%;
  background: rgba(10, 10, 26, 0.98);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px;
  flex-direction: column;
  gap: 10px;
  transform: translateY(-100%);
  opacity: 0;
  transition: all 0.3s ease;
}

.mobile-menu.open {
  transform: translateY(0);
  opacity: 1;
}

.mobile-link {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px 20px;
  text-decoration: none;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.mobile-link:hover,
.mobile-link.active {
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.mobile-icon {
  font-size: 1.3rem;
}

@media (max-width: 768px) {
  .nav-menu {
    display: none !important;
  }
  
  .nav-toggle {
    display: flex;
  }
  
  .mobile-menu {
    display: flex;
  }
  
  .floating-logo {
    top: 15px;
    left: 15px;
    padding: 10px 15px;
  }
  
  .logo-text {
    font-size: 1.1rem;
  }
  
  .logo-icon {
    font-size: 1.5rem;
  }
}
</style>
