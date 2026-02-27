<template>
  <div class="intellectual-page">
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="title-main">钟元智库</span>
          <span class="title-sub">Zhongyuan Think Tank</span>
        </h1>
        <p class="hero-description">
          钟元智库(数据知识产权)有限公司<br>
          汇聚智慧成果 · 守护创新价值
        </p>
        <div class="hero-stats">
          <div class="stat-item">
            <div class="stat-number">{{ stats.totalIP }}</div>
            <div class="stat-label">知识产权总数</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ stats.patents }}</div>
            <div class="stat-label">专利项目</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ stats.research }}</div>
            <div class="stat-label">研究成果</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ stats.contributors }}</div>
            <div class="stat-label">贡献者</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 登记流程 -->
    <section class="registration-section">
      <div class="section-header">
        <h2 class="section-title">登记流程</h2>
        <p class="section-subtitle">操作简单 · 高效快捷</p>
        <div class="section-line"></div>
      </div>
      <div class="registration-content">
        <div class="registration-visual">
          <div class="circular-network">
            <div class="network-node protection">保护</div>
            <div class="network-node registration">自助登记</div>
            <div class="network-node verification">校验</div>
            <div class="network-node certification">存证</div>
            <div class="network-node authentication">认证</div>
            <div class="network-node application">运用</div>
            <div class="center-logo">
              <div class="logo-circle">
                <div class="logo-text">钟元智库</div>
                <div class="logo-subtext">数据知识产权</div>
              </div>
            </div>
          </div>
        </div>
        <div class="registration-steps">
          <div class="step-item">
            <div class="step-number">1</div>
            <div class="step-title">办证申请</div>
          </div>
          <div class="step-item">
            <div class="step-number">2</div>
            <div class="step-title">联系我们</div>
          </div>
          <div class="step-item">
            <div class="step-number">3</div>
            <div class="step-title">公司公告</div>
          </div>
          <div class="step-item">
            <div class="step-number">4</div>
            <div class="step-title">证书查询</div>
          </div>
        </div>
      </div>
      <div class="registration-stats">
        <div class="stat-item">3435项</div>
        <div class="stat-item">3335项</div>
        <div class="stat-item">949个</div>
        <div class="stat-item">2011个</div>
        <div class="stat-item">114.0926亿条</div>
      </div>
    </section>

    <section class="search-section">
      <div class="search-container">
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="搜索知识产权、专利、研究成果..." 
            class="search-input"
          >
          <button class="search-btn">🔍</button>
        </div>
        <div class="filter-tags">
          <button 
            v-for="tag in filterTags" 
            :key="tag"
            :class="['filter-tag', { active: activeFilter === tag }]"
            @click="activeFilter = tag"
          >
            {{ tag }}
          </button>
        </div>
      </div>
    </section>

    <section class="ip-section">
      <div class="section-header">
        <h2 class="section-title">知识产权展示</h2>
        <div class="section-line"></div>
      </div>
      <div class="ip-grid">
        <div 
          v-for="ip in filteredIPs" 
          :key="ip.id" 
          class="ip-card"
          @click="showIPDetail(ip)"
        >
          <div class="ip-header">
            <span :class="['ip-type', ip.type]">{{ ip.typeLabel }}</span>
            <span class="ip-date">{{ ip.date }}</span>
          </div>
          <h3 class="ip-title">{{ ip.title }}</h3>
          <p class="ip-description">{{ ip.description }}</p>
          <div class="ip-footer">
            <span class="ip-author">👤 {{ ip.author }}</span>
            <span class="ip-status" :class="ip.status">{{ ip.statusLabel }}</span>
          </div>
        </div>
      </div>
    </section>

    <section class="categories-section">
      <div class="section-header">
        <h2 class="section-title">知识产权分类</h2>
        <div class="section-line"></div>
      </div>
      <div class="categories-grid">
        <div 
          v-for="category in categories" 
          :key="category.id" 
          class="category-card"
        >
          <div class="category-icon">{{ category.icon }}</div>
          <h3 class="category-title">{{ category.title }}</h3>
          <p class="category-description">{{ category.description }}</p>
          <div class="category-stats">
            <span class="category-count">{{ category.count }} 项</span>
          </div>
        </div>
      </div>
    </section>

    <section class="submit-section">
      <div class="submit-content">
        <h2>提交您的知识产权</h2>
        <p>欢迎广大修士提交您的研究成果和创新项目</p>
        <button class="btn btn-glow" @click="showSubmitForm = true">立即提交</button>
      </div>
    </section>

    <div v-if="showIPDetailModal" class="modal-overlay" @click="showIPDetailModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedIP?.title }}</h3>
          <button class="modal-close" @click="showIPDetailModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="detail-row">
            <span class="detail-label">类型：</span>
            <span class="detail-value">{{ selectedIP?.typeLabel }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">作者：</span>
            <span class="detail-value">{{ selectedIP?.author }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">日期：</span>
            <span class="detail-value">{{ selectedIP?.date }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">状态：</span>
            <span :class="['detail-value', 'status', selectedIP?.status]">{{ selectedIP?.statusLabel }}</span>
          </div>
          <div class="detail-description">
            <h4>详细描述</h4>
            <p>{{ selectedIP?.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showSubmitForm" class="modal-overlay" @click="showSubmitForm = false">
      <div class="modal-content submit-modal" @click.stop>
        <div class="modal-header">
          <h3>提交知识产权</h3>
          <button class="modal-close" @click="showSubmitForm = false">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitIP">
            <div class="form-group">
              <label>标题</label>
              <input type="text" v-model="submitForm.title" required>
            </div>
            <div class="form-group">
              <label>类型</label>
              <select v-model="submitForm.type" required>
                <option value="patent">专利</option>
                <option value="research">研究成果</option>
                <option value="copyright">版权</option>
                <option value="trademark">商标</option>
              </select>
            </div>
            <div class="form-group">
              <label>描述</label>
              <textarea v-model="submitForm.description" rows="4" required></textarea>
            </div>
            <div class="form-group">
              <label>作者</label>
              <input type="text" v-model="submitForm.author" required>
            </div>
            <button type="submit" class="btn btn-primary">提交</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const stats = ref({
  totalIP: 128,
  patents: 45,
  research: 67,
  contributors: 32
})

const searchQuery = ref('')
const activeFilter = ref('全部')
const filterTags = ['全部', '专利', '研究成果', '版权', '商标']

const showIPDetailModal = ref(false)
const showSubmitForm = ref(false)
const selectedIP = ref(null)

const submitForm = ref({
  title: '',
  type: 'patent',
  description: '',
  author: ''
})

const ipData = ref([
  {
    id: 1,
    type: 'patent',
    typeLabel: '专利',
    title: '量子符文算法',
    description: '一种结合量子计算与传统符文的创新算法，大幅提升空间站数据处理效率。',
    author: '钟元',
    date: '2025-01-15',
    status: 'approved',
    statusLabel: '已认证'
  },
  {
    id: 2,
    type: 'research',
    typeLabel: '研究成果',
    title: '空间站能量场优化研究',
    description: '通过分析空间站能量场分布，提出优化方案，提升整体稳定性30%。',
    author: 'xinrenleiZZY',
    date: '2025-02-20',
    status: 'approved',
    statusLabel: '已认证'
  },
  {
    id: 3,
    type: 'copyright',
    typeLabel: '版权',
    title: '聚星数据流加密协议',
    description: '专用于聚星空间站数据传输的加密协议，确保信息安全。',
    author: '安全团队',
    date: '2025-03-10',
    status: 'pending',
    statusLabel: '审核中'
  },
  {
    id: 4,
    type: 'research',
    typeLabel: '研究成果',
    title: '修仙与科技融合理论',
    description: '探索修仙符文与现代科技结合的理论基础，为后续研究提供指导。',
    author: '研究组A',
    date: '2025-04-05',
    status: 'approved',
    statusLabel: '已认证'
  },
  {
    id: 5,
    type: 'patent',
    typeLabel: '专利',
    title: '意识上传稳定器',
    description: '确保意识上传过程稳定性的关键设备，大幅降低上传风险。',
    author: '技术团队',
    date: '2025-05-12',
    status: 'approved',
    statusLabel: '已认证'
  },
  {
    id: 6,
    type: 'trademark',
    typeLabel: '商标',
    title: '聚星空间站标识',
    description: '聚星空间站的官方标识，象征智慧与探索的精神。',
    author: '设计团队',
    date: '2025-06-01',
    status: 'approved',
    statusLabel: '已认证'
  }
])

const categories = ref([
  {
    id: 1,
    icon: '⚡',
    title: '算法专利',
    description: '核心算法与技术创新的专利保护',
    count: 45
  },
  {
    id: 2,
    icon: '🔬',
    title: '研究成果',
    description: '科学研究与实验成果的知识产权',
    count: 67
  },
  {
    id: 3,
    icon: '📜',
    title: '版权作品',
    description: '文学、艺术、软件等原创作品',
    count: 23
  },
  {
    id: 4,
    icon: '🏷️',
    title: '商标品牌',
    description: '品牌标识与商业标识的注册保护',
    count: 15
  }
])

const filteredIPs = computed(() => {
  let filtered = ipData.value

  if (activeFilter.value !== '全部') {
    const typeMap = {
      '专利': 'patent',
      '研究成果': 'research',
      '版权': 'copyright',
      '商标': 'trademark'
    }
    filtered = filtered.filter(ip => ip.type === typeMap[activeFilter.value])
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(ip => 
      ip.title.toLowerCase().includes(query) ||
      ip.description.toLowerCase().includes(query) ||
      ip.author.toLowerCase().includes(query)
    )
  }

  return filtered
})

const showIPDetail = (ip) => {
  selectedIP.value = ip
  showIPDetailModal.value = true
}

const submitIP = () => {
  alert('知识产权提交成功！')
  showSubmitForm.value = false
  submitForm.value = {
    title: '',
    type: 'patent',
    description: '',
    author: ''
  }
}
</script>

<style scoped>
.intellectual-page {
  min-height: 100vh;
  position: relative;
  z-index: 1;
}

.hero-section {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  position: relative;
}

.hero-content {
  text-align: center;
  max-width: 1000px;
}

.hero-title {
  margin-bottom: 30px;
}

.title-main {
  display: block;
  font-size: 3.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 10px;
}

.title-sub {
  display: block;
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.7);
  letter-spacing: 6px;
  text-transform: uppercase;
}

.hero-description {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.8;
  margin-bottom: 50px;
}

.hero-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 30px;
  margin-top: 60px;
}

.stat-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 30px 20px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-5px);
  border-color: rgba(150, 200, 255, 0.3);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 10px;
}

.stat-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

section {
  padding: 80px 20px;
}

.section-header {
  text-align: center;
  margin-bottom: 50px;
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

.section-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
  margin-bottom: 20px;
}

/* 登记流程 */
.registration-section {
  padding: 100px 20px;
  background: rgba(10, 10, 30, 0.8);
  position: relative;
}

.registration-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1), rgba(240, 147, 251, 0.1));
  z-index: 1;
}

.registration-content {
  position: relative;
  z-index: 2;
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 60px;
}

.registration-visual {
  flex: 1;
  min-width: 400px;
  position: relative;
}

.circular-network {
  position: relative;
  width: 400px;
  height: 400px;
  margin: 0 auto;
}

.network-node {
  position: absolute;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: white;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.network-node:hover {
  transform: scale(1.1);
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
}

.network-node.protection {
  top: 20px;
  left: 50px;
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.network-node.registration {
  top: 60px;
  right: 80px;
  background: rgba(46, 204, 113, 0.2);
  border-color: #2ecc71;
}

.network-node.verification {
  bottom: 80px;
  right: 60px;
  background: rgba(52, 152, 219, 0.2);
  border-color: #3498db;
}

.network-node.certification {
  top: 150px;
  left: 30px;
  background: rgba(241, 196, 15, 0.2);
  border-color: #f1c40f;
}

.network-node.authentication {
  bottom: 120px;
  left: 100px;
  background: rgba(231, 76, 60, 0.2);
  border-color: #e74c3c;
}

.network-node.application {
  bottom: 40px;
  right: 120px;
  background: rgba(155, 89, 182, 0.2);
  border-color: #9b59b6;
}

.center-logo {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.logo-circle {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
  border: 3px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(15px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 5px;
  text-align: center;
}

.logo-subtext {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  text-align: center;
}

.registration-steps {
  flex: 1;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.step-item:hover {
  transform: translateX(10px);
  border-color: rgba(102, 126, 234, 0.3);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.step-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.registration-stats {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 60px auto 0;
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
}

.registration-stats .stat-item {
  font-size: 1.3rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  text-align: center;
  padding: 15px 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  backdrop-filter: blur(10px);
}

.search-section {
  background: rgba(255, 255, 255, 0.02);
}

.search-container {
  max-width: 800px;
  margin: 0 auto;
}

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
}

.search-input {
  flex: 1;
  padding: 15px 20px;
  font-size: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 50px;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  background: rgba(255, 255, 255, 0.1);
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-btn {
  width: 50px;
  height: 50px;
  border: none;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-btn:hover {
  transform: scale(1.1);
}

.filter-tags {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

.filter-tag {
  padding: 8px 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.filter-tag:hover,
.filter-tag.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
}

.ip-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
  max-width: 1400px;
  margin: 0 auto;
}

.ip-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 30px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  cursor: pointer;
}

.ip-card:hover {
  transform: translateY(-5px);
  border-color: rgba(150, 200, 255, 0.3);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.ip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.ip-type {
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.ip-type.patent {
  background: rgba(102, 126, 234, 0.2);
  color: #667eea;
}

.ip-type.research {
  background: rgba(240, 147, 251, 0.2);
  color: #f093fb;
}

.ip-type.copyright {
  background: rgba(100, 255, 200, 0.2);
  color: #64ffc8;
}

.ip-type.trademark {
  background: rgba(255, 200, 100, 0.2);
  color: #ffc864;
}

.ip-date {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.85rem;
}

.ip-title {
  color: white;
  font-size: 1.3rem;
  margin-bottom: 15px;
}

.ip-description {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  margin-bottom: 20px;
}

.ip-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.ip-author {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
}

.ip-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.ip-status.approved {
  background: rgba(100, 255, 150, 0.2);
  color: #64ff96;
}

.ip-status.pending {
  background: rgba(255, 200, 100, 0.2);
  color: #ffc864;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.category-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 40px 30px;
  text-align: center;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.category-card:hover {
  transform: translateY(-10px);
  border-color: rgba(150, 200, 255, 0.3);
}

.category-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.category-title {
  color: white;
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.category-description {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  margin-bottom: 20px;
}

.category-count {
  color: #667eea;
  font-weight: 600;
  font-size: 1.1rem;
}

.submit-section {
  text-align: center;
  padding: 120px 20px;
}

.submit-content h2 {
  font-size: 2.5rem;
  color: white;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.submit-content p {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 40px;
}

.btn {
  padding: 15px 40px;
  font-size: 1.1rem;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.modal-content {
  background: rgba(20, 20, 40, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 40px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  backdrop-filter: blur(20px);
}

.submit-modal {
  max-width: 500px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
  color: white;
  font-size: 1.5rem;
}

.modal-close {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  font-size: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.modal-close:hover {
  color: white;
}

.modal-body {
  color: rgba(255, 255, 255, 0.9);
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 15px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.detail-label {
  color: rgba(255, 255, 255, 0.6);
  font-weight: 600;
}

.detail-value {
  color: white;
}

.detail-value.status.approved {
  color: #64ff96;
}

.detail-value.status.pending {
  color: #ffc864;
}

.detail-description {
  margin-top: 30px;
}

.detail-description h4 {
  color: white;
  margin-bottom: 15px;
}

.detail-description p {
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.8);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 8px;
  font-weight: 600;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  background: rgba(255, 255, 255, 0.1);
}

.form-group textarea {
  resize: vertical;
}

@media (max-width: 768px) {
  .title-main {
    font-size: 2.5rem;
  }
  
  .title-sub {
    font-size: 1rem;
    letter-spacing: 3px;
  }
  
  .hero-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .ip-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    padding: 30px 20px;
  }
}
</style>
