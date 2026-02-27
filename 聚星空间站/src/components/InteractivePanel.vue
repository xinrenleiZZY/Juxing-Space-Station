<template>
  <div class="interactive-panel">
    <div class="panel-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        {{ tab.label }}
      </button>
    </div>

    <div class="panel-content">
      <div v-if="activeTab === 'message'" class="tab-content">
        <h3>留言板</h3>
        <form @submit.prevent="submitMessage" class="message-form">
          <div class="form-group">
            <label>您的称呼</label>
            <input type="text" v-model="messageForm.name" placeholder="请输入您的称呼" required>
          </div>
          <div class="form-group">
            <label>留言内容</label>
            <textarea 
              v-model="messageForm.content" 
              placeholder="分享您的想法..." 
              rows="4" 
              required
            ></textarea>
          </div>
          <button type="submit" class="btn btn-primary">提交留言</button>
        </form>

        <div class="messages-list">
          <div v-for="(msg, index) in messages" :key="index" class="message-item">
            <div class="message-header">
              <span class="message-author">{{ msg.name }}</span>
              <span class="message-time">{{ msg.time }}</span>
            </div>
            <p class="message-content">{{ msg.content }}</p>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'register'" class="tab-content">
        <h3>修士注册</h3>
        <form @submit.prevent="submitRegister" class="register-form">
          <div class="form-group">
            <label>修士名称</label>
            <input type="text" v-model="registerForm.name" placeholder="请输入修士名称" required>
          </div>
          <div class="form-group">
            <label>邮箱地址</label>
            <input type="email" v-model="registerForm.email" placeholder="请输入邮箱地址" required>
          </div>
          <div class="form-group">
            <label>修炼方向</label>
            <select v-model="registerForm.direction" required>
              <option value="">请选择修炼方向</option>
              <option value="tech">科技修仙</option>
              <option value="algorithm">算法符文</option>
              <option value="data">数据炼化</option>
              <option value="security">安全防护</option>
              <option value="other">其他</option>
            </select>
          </div>
          <div class="form-group">
            <label>个人简介</label>
            <textarea 
              v-model="registerForm.bio" 
              placeholder="介绍一下自己..." 
              rows="3"
            ></textarea>
          </div>
          <button type="submit" class="btn btn-primary">注册成为修士</button>
        </form>
      </div>

      <div v-if="activeTab === 'explore'" class="tab-content">
        <h3>提交探索记录</h3>
        <form @submit.prevent="submitExplore" class="explore-form">
          <div class="form-group">
            <label>探索标题</label>
            <input type="text" v-model="exploreForm.title" placeholder="请输入探索标题" required>
          </div>
          <div class="form-group">
            <label>探索类型</label>
            <select v-model="exploreForm.type" required>
              <option value="">请选择探索类型</option>
              <option value="discovery">新发现</option>
              <option value="research">研究成果</option>
              <option value="experience">探索经验</option>
              <option value="question">疑问与思考</option>
            </select>
          </div>
          <div class="form-group">
            <label>详细描述</label>
            <textarea 
              v-model="exploreForm.description" 
              placeholder="详细描述您的探索过程和发现..." 
              rows="6" 
              required
            ></textarea>
          </div>
          <div class="form-group">
            <label>相关标签（用逗号分隔）</label>
            <input 
              type="text" 
              v-model="exploreForm.tags" 
              placeholder="例如：算法,符文,数据流"
            >
          </div>
          <button type="submit" class="btn btn-primary">提交探索记录</button>
        </form>

        <div class="explore-stats">
          <h4>探索统计</h4>
          <div class="stats-grid">
            <div class="stat-box">
              <div class="stat-number">{{ exploreStats.total }}</div>
              <div class="stat-label">总记录数</div>
            </div>
            <div class="stat-box">
              <div class="stat-number">{{ exploreStats.today }}</div>
              <div class="stat-label">今日新增</div>
            </div>
            <div class="stat-box">
              <div class="stat-number">{{ exploreStats.explorers }}</div>
              <div class="stat-label">活跃探索者</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('message')

const tabs = [
  { id: 'message', label: '留言板' },
  { id: 'register', label: '修士注册' },
  { id: 'explore', label: '探索记录' }
]

const messageForm = ref({
  name: '',
  content: ''
})

const registerForm = ref({
  name: '',
  email: '',
  direction: '',
  bio: ''
})

const exploreForm = ref({
  title: '',
  type: '',
  description: '',
  tags: ''
})

const messages = ref([
  {
    name: '探索者A',
    content: '聚星空间站真是一个神奇的地方，修仙与科技的完美融合！',
    time: '2025-01-15 14:30'
  },
  {
    name: '数据修士',
    content: '感谢ZZY开放这个空间，让我们能够自由探索未知领域。',
    time: '2025-01-16 09:20'
  },
  {
    name: '符文师',
    content: '这里的符文算法太精妙了，值得深入研究。',
    time: '2025-01-17 16:45'
  }
])

const exploreStats = ref({
  total: 156,
  today: 12,
  explorers: 43
})

const submitMessage = () => {
  const newMessage = {
    name: messageForm.value.name,
    content: messageForm.value.content,
    time: new Date().toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
  messages.value.unshift(newMessage)
  messageForm.value = { name: '', content: '' }
  alert('留言提交成功！')
}

const submitRegister = () => {
  alert(`欢迎 ${registerForm.value.name} 加入聚星空间站！注册成功！`)
  registerForm.value = {
    name: '',
    email: '',
    direction: '',
    bio: ''
  }
}

const submitExplore = () => {
  exploreStats.value.total++
  exploreStats.value.today++
  alert('探索记录提交成功！感谢您的贡献！')
  exploreForm.value = {
    title: '',
    type: '',
    description: '',
    tags: ''
  }
}
</script>

<style scoped>
.interactive-panel {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  max-width: 800px;
  margin: 0 auto;
}

.panel-tabs {
  display: flex;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(0, 0, 0, 0.2);
}

.tab-btn {
  flex: 1;
  padding: 20px;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.tab-btn:hover {
  color: rgba(255, 255, 255, 0.9);
  background: rgba(255, 255, 255, 0.05);
}

.tab-btn.active {
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.panel-content {
  padding: 40px;
}

.tab-content h3 {
  color: white;
  font-size: 1.8rem;
  margin-bottom: 30px;
  text-align: center;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 10px;
  font-weight: 600;
  font-size: 1rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 15px 20px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.2);
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.btn {
  width: 100%;
  padding: 18px 30px;
  font-size: 1.1rem;
  border: none;
  border-radius: 12px;
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
  transform: translateY(-2px);
  box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
}

.messages-list {
  margin-top: 40px;
  padding-top: 40px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.message-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 15px;
  transition: all 0.3s ease;
}

.message-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(150, 200, 255, 0.2);
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.message-author {
  color: #667eea;
  font-weight: 600;
  font-size: 1.1rem;
}

.message-time {
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.9rem;
}

.message-content {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin: 0;
}

.explore-stats {
  margin-top: 40px;
  padding-top: 40px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.explore-stats h4 {
  color: white;
  font-size: 1.3rem;
  margin-bottom: 20px;
  text-align: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat-box {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 25px 15px;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-box:hover {
  transform: translateY(-5px);
  border-color: rgba(150, 200, 255, 0.3);
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 8px;
}

.stat-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .panel-content {
    padding: 25px 20px;
  }
  
  .tab-btn {
    padding: 15px 10px;
    font-size: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-box {
    padding: 20px;
  }
}
</style>
