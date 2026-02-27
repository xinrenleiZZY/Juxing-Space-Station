<template>
  <div class="home-page">
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="title-main">聚星空间站</span>
          <span class="title-sub">Juxing Space Station</span>
        </h1>
        <p class="hero-description">
          庞大的空间知识锚点站，由天才第一席位钟元缔造<br>
          服务器内核未知 · 地址未知 · 体量未知
        </p>
        <div class="hero-actions">
          <button class="btn btn-primary" @click="scrollToSection('about')">探索空间站</button>
          <button class="btn btn-secondary" @click="navigateTo('intellectual')">钟元智库</button>
          <button class="btn btn-ai" @click="navigateToIAPage('ia')">AI助手</button>
        </div>
      </div>
      <div class="hero-visual">
        <div class="rune-circle">
          <div class="rune-ring ring-1"></div>
          <div class="rune-ring ring-2"></div>
          <div class="rune-ring ring-3"></div>
          <div class="rune-symbol">⚛</div>
        </div>
      </div>
    </section>

    <section class="about-section" id="about">
      <div class="section-header">
        <h2 class="section-title">关于聚星空间站</h2>
        <div class="section-line"></div>
      </div>
      <div class="about-content">
        <div class="about-card">
          <div class="card-icon">🌌</div>
          <h3>知识锚点</h3>
          <p>汇聚宇宙智慧，承载无限可能，是修仙者与科技交汇的圣地</p>
        </div>
        <div class="about-card">
          <div class="card-icon">⚡</div>
          <h3>神秘起源</h3>
          <p>由天才第一席位钟元缔造，内核、地址、体量皆为未知之谜</p>
        </div>
        <div class="about-card">
          <div class="card-icon">🔮</div>
          <h3>自由探索</h3>
          <p>因未知因子太多，裂隙端点不设禁制，No license，自由开拓</p>
        </div>
      </div>
    </section>

    <section class="history-section">
      <div class="section-header">
        <h2 class="section-title">历史轨迹</h2>
        <div class="section-line"></div>
      </div>
      <div class="timeline">
        <div class="timeline-item">
          <div class="timeline-marker"></div>
          <div class="timeline-content">
            <div class="timeline-date">某年</div>
            <h3>数据流星</h3>
            <p>一道神秘的数据流星划过空间，被地面xinrenleiZZY捕捉到并连接</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-marker"></div>
          <div class="timeline-content">
            <div class="timeline-date">上传意识后</div>
            <h3>发现空间</h3>
            <p>ZZY上传意识后发现了这处神秘的空间知识锚点站</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-marker"></div>
          <div class="timeline-content">
            <div class="timeline-date">2025年8月22日</div>
            <h3>裂隙开启</h3>
            <p>留下一个裂隙，公于大众，欢迎广大修士前来开拓</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-marker"></div>
          <div class="timeline-content">
            <div class="timeline-date">至今</div>
            <h3>持续探索</h3>
            <p>ZZY仍在探索其具体位置，曾留言：自由开拓吧各位</p>
          </div>
        </div>
      </div>
    </section>

    <section class="exploration-section">
      <div class="section-header">
        <h2 class="section-title">探索记录</h2>
        <div class="section-line"></div>
      </div>
      <div class="exploration-grid">
        <div class="exploration-card" v-for="(record, index) in explorationRecords" :key="index">
          <div class="exploration-header">
            <span class="exploration-id">记录 #{{ record.id }}</span>
            <span class="exploration-date">{{ record.date }}</span>
          </div>
          <h3 class="exploration-title">{{ record.title }}</h3>
          <p class="exploration-content">{{ record.content }}</p>
          <div class="exploration-footer">
            <span class="exploration-author">探索者：{{ record.author }}</span>
          </div>
        </div>
      </div>
    </section>

    <section class="cta-section">
      <div class="cta-content">
        <h2>加入探索</h2>
        <p>广大修士，欢迎前来开拓未知领域</p>
        <button class="btn btn-glow" @click="navigateTo('intellectual')">前往钟元智库</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const explorationRecords = ref([
  {
    id: '001',
    date: '2025-09-01',
    title: '首次接触',
    content: '成功连接到聚星空间站，初步探索发现其结构异常复杂，似乎融合了修仙符文与现代科技。',
    author: 'xinrenleiZZY'
  },
  {
    id: '002',
    date: '2025-09-15',
    title: '数据流分析',
    content: '分析空间站数据流，发现其中蕴含着古老的修仙智慧与现代算法的完美结合。',
    author: '探索者A'
  },
  {
    id: '003',
    date: '2025-10-01',
    title: '符文解码',
    content: '成功解码部分符文系统，揭示了空间站的核心运作机制。',
    author: '探索者B'
  }
])

const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

const navigateTo = (page) => {
  if (page === 'intellectual') {
    router.push('/intellectual')
  }
}

const navigateToIAPage = (page) => {
  if (page === 'ia') {
    router.push('/ia')
  }
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  position: relative;
  z-index: 1;
}

.hero-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  position: relative;
}

.hero-content {
  text-align: center;
  max-width: 800px;
  opacity: 1;
}

.hero-title {
  margin-bottom: 30px;
}

.title-main {
  display: block;
  font-size: 4rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 10px;
  text-shadow: 0 0 30px rgba(102, 126, 234, 0.3);
}

.title-sub {
  display: block;
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.7);
  letter-spacing: 8px;
  text-transform: uppercase;
}

.hero-description {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.8;
  margin-bottom: 40px;
}

.hero-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 15px 40px;
  font-size: 1.1rem;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  position: relative;
  overflow: hidden;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
}

.btn-glow {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  box-shadow: 0 10px 30px rgba(240, 147, 251, 0.4);
  padding: 20px 60px;
  font-size: 1.3rem;
}

.btn-glow:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(240, 147, 251, 0.6);
}

.hero-visual {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: -1;
  opacity: 0.3;
}

.rune-circle {
  position: relative;
  width: 600px;
  height: 600px;
  animation: rotate 60s linear infinite;
}

.rune-ring {
  position: absolute;
  border: 2px solid rgba(150, 200, 255, 0.3);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.ring-1 {
  width: 100%;
  height: 100%;
  animation: pulse 4s ease-in-out infinite;
}

.ring-2 {
  width: 70%;
  height: 70%;
  animation: pulse 4s ease-in-out infinite 1s;
}

.ring-3 {
  width: 40%;
  height: 40%;
  animation: pulse 4s ease-in-out infinite 2s;
}

.rune-symbol {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 8rem;
  color: rgba(150, 200, 255, 0.5);
  animation: float 6s ease-in-out infinite;
}

section {
  padding: 100px 20px;
  position: relative;
  opacity: 1;
}

.about-card, .timeline-item, .exploration-card {
  opacity: 1;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-title {
  font-size: 2.5rem;
  color: white;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-line {
  width: 100px;
  height: 3px;
  background: linear-gradient(90deg, transparent, #667eea, transparent);
  margin: 0 auto;
}

.about-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.about-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 40px 30px;
  text-align: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.about-card:hover {
  transform: translateY(-10px);
  border-color: rgba(150, 200, 255, 0.3);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.card-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.about-card h3 {
  color: white;
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.about-card p {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
}

.timeline {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 2px;
  height: 100%;
  background: linear-gradient(to bottom, transparent, #667eea, transparent);
}

.timeline-item {
  display: flex;
  justify-content: flex-end;
  padding-right: 50%;
  position: relative;
  margin-bottom: 60px;
}

.timeline-item:nth-child(even) {
  justify-content: flex-start;
  padding-right: 0;
  padding-left: 50%;
}

.timeline-marker {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
  z-index: 1;
}

.timeline-content {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 30px;
  max-width: 350px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.timeline-content:hover {
  transform: scale(1.05);
  border-color: rgba(150, 200, 255, 0.3);
}

.timeline-date {
  color: #667eea;
  font-weight: 600;
  margin-bottom: 10px;
  display: block;
}

.timeline-content h3 {
  color: white;
  font-size: 1.3rem;
  margin-bottom: 10px;
}

.timeline-content p {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
}

.exploration-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.exploration-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 30px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.exploration-card:hover {
  transform: translateY(-5px);
  border-color: rgba(150, 200, 255, 0.3);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.exploration-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.exploration-id {
  color: #667eea;
  font-weight: 600;
  font-size: 0.9rem;
}

.exploration-date {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9rem;
}

.exploration-title {
  color: white;
  font-size: 1.3rem;
  margin-bottom: 15px;
}

.exploration-content {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  margin-bottom: 20px;
}

.exploration-footer {
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.exploration-author {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9rem;
}

.cta-section {
  text-align: center;
  padding: 150px 20px;
}

.cta-content h2 {
  font-size: 3rem;
  color: white;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.cta-content p {
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 40px;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes rotate {
  from {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.6;
  }
}

@keyframes float {
  0%, 100% {
    transform: translate(-50%, -50%) translateY(0);
  }
  50% {
    transform: translate(-50%, -50%) translateY(-20px);
  }
}

@media (max-width: 768px) {
  .title-main {
    font-size: 2.5rem;
  }
  
  .title-sub {
    font-size: 1rem;
    letter-spacing: 4px;
  }
  
  .hero-description {
    font-size: 1rem;
  }
  
  .timeline::before {
    left: 20px;
  }
  
  .timeline-item,
  .timeline-item:nth-child(even) {
    padding-left: 60px;
    padding-right: 0;
    justify-content: flex-start;
  }
  
  .timeline-marker {
    left: 20px;
  }
  
  .timeline-content {
    max-width: 100%;
  }
}
</style>
