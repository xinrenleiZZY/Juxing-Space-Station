<template>
  <div class="ai-assistant-page">
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="title-main">AI 助手</span>
          <span class="title-sub">AI Assistant</span>
        </h1>
        <p class="hero-description">
          钟元智库智能助手 · 数据知识产权专业咨询<br>
          支持智能问答和业务咨询
        </p>
      </div>
    </section>

    <section class="chat-section">
      <div class="section-header">
        <h2 class="section-title">智能对话</h2>
        <div class="section-line"></div>
      </div>
      
      <div class="chat-container">
        <!-- 聊天记录区域 -->
        <div class="chat-messages" ref="chatMessages">
          <!-- 系统消息 -->
          <div class="message system-message">
            <div class="message-content">
              <p>你好！我是钟元智库的智能助手。我可以为您提供数据知识产权相关的咨询服务。</p>
            </div>
          </div>
          
          <!-- 聊天消息 -->
          <div 
            v-for="(message, index) in messages" 
            :key="index"
            :class="[`message`, message.role]"
          >
            <div class="message-avatar">
              {{ message.role === 'user' ? '👤' : '🤖' }}
            </div>
            <div class="message-content">
              <!-- 文本内容 -->
              <div v-if="message.content.text" class="message-text" :class="{ streaming: message.streaming }">
                {{ message.content.text }}
              </div>
              <!-- 图片内容 -->
              <div v-if="message.content.image" class="message-image">
                <img :src="message.content.image" :alt="'Message image'">
              </div>
            </div>
          </div>
          
          <!-- 加载中消息 -->
          <div v-if="isStreaming" class="message assistant-message">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
              <div class="loading-indicator">
                <span class="loading-dot"></span>
                <span class="loading-dot"></span>
                <span class="loading-dot"></span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 输入区域 -->
        <div class="chat-input-area">
          <!-- 顶部工具栏 -->
          <div class="input-toolbar">
            <!-- 上传按钮 -->
            <div class="upload-buttons">
              <button 
                class="btn btn-icon"
                @click="triggerFileInput"
                title="上传图片"
                :disabled="isLoading || isStreaming"
              >
                🖼️
              </button>
              <input 
                type="file" 
                ref="fileInput"
                accept="image/*"
                class="file-input"
                @change="handleImageUpload"
                style="display: none"
              >
              
              <!-- 模型测试按钮 -->
              <button 
                class="btn btn-icon"
                @click="testAllModels"
                title="测试所有模型"
                :disabled="isTestingModels || isLoading || isStreaming"
              >
                🧪
              </button>
              
              <!-- 停止按钮 -->
              <button 
                class="btn btn-icon"
                @click="stopGeneration"
                title="停止生成"
                :disabled="!isStreaming"
                v-if="isStreaming"
              >
                ⏹️
              </button>
              
              <!-- 模型选择 -->
              <div class="model-selector">
                <select 
                  v-model="selectedModel"
                  class="model-select"
                  :disabled="isLoading || isStreaming"
                >
                  <option 
                    v-for="model in models" 
                    :key="model.id"
                    :value="model.id"
                  >
                    {{ model.name }}
                    <span v-if="modelTestStatus[model.id]" class="model-status">
                      {{ modelTestStatus[model.id] === 'valid' ? ' ✅' : modelTestStatus[model.id] === 'invalid' ? ' ❌' : ' ⏳' }}
                    </span>
                  </option>
                </select>
              </div>
            </div>
          </div>
          
          <!-- 文本输入 -->
          <div class="text-input-section">
            <div class="text-input-container">
              <input 
                type="text" 
                v-model="inputText"
                placeholder="输入你的问题..."
                class="text-input"
                @keyup.enter="sendMessage"
                :disabled="isLoading || isStreaming"
              >
              <button 
                class="btn btn-primary"
                @click="sendMessage"
                :disabled="isLoading || isStreaming || !inputText.trim()"
              >
                {{ isStreaming ? '生成中...' : isLoading ? '发送中...' : '发送' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="features-section">
      <div class="section-header">
        <h2 class="section-title">服务特点</h2>
        <div class="section-line"></div>
      </div>
      <div class="features-content">
        <div class="feature-card">
          <div class="feature-icon">📋</div>
          <h3>业务咨询</h3>
          <p>提供专业的数据知识产权登记、保护、运用等业务咨询服务</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💬</div>
          <h3>智能问答</h3>
          <p>支持连续提问，智能助手会根据上下文理解您的需求</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🤖</div>
          <h3>专业服务</h3>
          <p>基于钟元智库的专业知识库，为您提供精准的解答</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'

// 响应式数据
const chatMessages = ref(null)
const messages = ref([])
const inputText = ref('')
const apiKey = ref('a3e3e754-162c-4bf3-b9b6-7519784e4f00')
const isLoading = ref(false)
const isStreaming = ref(false)

// 模型配置 - 使用正确的模型ID和友好的中文名称
const models = ref([
  // { id: 'doubao-1.5-vision-pro-250328', name: '豆包 1.5 视觉 Pro' },
  // { id: 'doubao-1-5-vision-lite-2500315', name: '豆包 1.5 视觉 Lite' },
  // { id: 'doubao-1-5-thinking-pro-250415', name: '豆包 1.5 思考 Pro' },
  // { id: 'doubao-1-5-ui-tars-250428', name: '豆包 1.5 UI TARS' },
  { id: 'doubao-1-5-vision-pro-32k-250115', name: '豆包 1.5 视觉 Pro 32k' },
  // { id: 'doubao-1-5-pro-256k-250115', name: '豆包 1.5 Pro 256k' },
  { id: 'doubao-1-5-lite-32k-250115', name: '豆包 1.5 Lite 32k' },
  { id: 'doubao-1-5-pro-32k-250115', name: '豆包 1.5 Pro 32k' },
  { id: 'doubao-seed-1-8-251228', name: '豆包种子 1.8' },
  // { id: 'doubao-seed-code-preview-251028', name: '豆包种子 Code' },
  { id: 'doubao-seed-1-6-lite-251015', name: '豆包种子 1.6 Lite' },
  // { id: 'doubao-seed-translation-250915', name: '豆包种子 翻译' },
  { id: 'doubao-seed-1-6-vision-250815', name: '豆包种子 1.6 视觉' },
  { id: 'doubao-seed-1-6-251015', name: '豆包种子 1.6' },
  // { id: 'doubao-seed-1-6-thinking-250715', name: '豆包种子 1.6 思考' },
  { id: 'doubao-seed-1-6-flash-250828', name: '豆包种子 1.6 Flash' },
  // { id: 'doubao-seedance-1-5-pro-251215', name: '豆包 Seedance 1.5 Pro' },
  // { id: 'doubao-seedance-1-0-pro-250528', name: '豆包 Seedance 1.0 Pro' },
  // { id: 'doubao-seedance-1-0-lite-t2v-250428', name: '豆包 Seedance 1.0 Lite T2V' },
  // { id: 'doubao-seedance-1-0-lite-i2v-250428', name: '豆包 Seedance 1.0 Lite I2V' },
  // { id: 'doubao-seedream-4-5-251128', name: '豆包 Seedream 4.5' },
  // { id: 'doubao-seedream-4-0-250828', name: '豆包 Seedream 4.0' },
  { id: 'deepseek-v3-2-251201', name: 'DeepSeek V3.2' },
  { id: 'deepseek-v3-1-terminus', name: 'DeepSeek V3.1' },
  { id: 'deepseek-r1-250528', name: 'DeepSeek R1' },
  { id: 'deepseek-v3-250324', name: 'DeepSeek V3' },
  { id: 'kimi-k2-thinking-251104', name: 'Kimi K2' },
  { id: 'glm-4-7-251222', name: 'GLM 4.7' }
])
const selectedModel = ref('doubao-1.5-vision-pro-250328')

const API_BASE_URL = 'https://ark.cn-beijing.volces.com/api/v3'

// 模型测试状态
const modelTestStatus = ref({})
const isTestingModels = ref(false)

// 生成控制
const shouldCancelGeneration = ref(false)

// 测试模型可用性
const testModel = async (modelId) => {
  try {
    const url = `${API_BASE_URL}/chat/completions`
    
    const payload = {
      model: modelId,
      messages: [
        {
          role: 'user',
          content: '测试模型可用性'
        }
      ],
      stream: false,
      max_tokens: 1
    }

    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey.value}`
      },
      body: JSON.stringify(payload)
    })

    if (res.ok) {
      return true
    } else {
      return false
    }
  } catch (error) {
    return false
  }
}

// 批量测试所有模型
const testAllModels = async () => {
  isTestingModels.value = true
  modelTestStatus.value = {}
  
  const validModels = []
  
  for (const model of models.value) {
    modelTestStatus.value[model.id] = 'testing'
    
    const isAvailable = await testModel(model.id)
    
    if (isAvailable) {
      modelTestStatus.value[model.id] = 'valid'
      validModels.push(model)
    } else {
      modelTestStatus.value[model.id] = 'invalid'
    }
  }
  
  // 更新为仅包含有效模型
  models.value = validModels
  isTestingModels.value = false
}

// 停止生成
const stopGeneration = () => {
  shouldCancelGeneration.value = true
  isLoading.value = false
  isStreaming.value = false
}

// 发送消息
const sendMessage = async () => {
  if (!inputText.value.trim() || isLoading.value) return
  
  // 重置取消标志
  shouldCancelGeneration.value = false
  
  // 添加用户消息到聊天记录
  const userMessage = {
    role: 'user',
    content: {
      text: inputText.value.trim()
    }
  }
  messages.value.push(userMessage)
  
  // 清空输入
  const question = inputText.value.trim()
  inputText.value = ''
  
  // 滚动到底部
  await nextTick()
  scrollToBottom()
  
  // 调用 API
  await callAPI(question)
}

// 滚动到聊天底部
const scrollToBottom = () => {
  if (chatMessages.value) {
    chatMessages.value.scrollTop = chatMessages.value.scrollHeight
  }
}

// 触发文件选择
const fileInput = ref(null)
const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

// 处理图片上传
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      const imageData = e.target.result
      
      // 添加图片消息到聊天记录
      const imageMessage = {
        role: 'user',
        content: {
          image: imageData
        }
      }
      messages.value.push(imageMessage)
      
      // 滚动到底部
      nextTick(() => {
        scrollToBottom()
      })
    }
    reader.readAsDataURL(file)
  }
}

// 调用 API
const callAPI = async (question) => {
  isLoading.value = true
  isStreaming.value = true
  
  try {
    const url = `${API_BASE_URL}/chat/completions`
    
    // 构建请求数据
    const payload = {
      model: selectedModel.value,
      messages: [
        {
          role: 'user',
          content: question
        }
      ],
      stream: true
    }

    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey.value}`
      },
      body: JSON.stringify(payload)
    })

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}))
      throw new Error(`HTTP error! status: ${res.status}, message: ${JSON.stringify(errorData)}`)
    }

    // 处理流式响应
    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    
    // 创建临时助手消息
    const assistantMessageId = messages.value.length
    const assistantMessage = {
      role: 'assistant',
      content: {
        text: ''
      },
      streaming: true
    }
    messages.value.push(assistantMessage)
    
    // 滚动到底部
    await nextTick()
    scrollToBottom()
    
    // 逐块读取响应
    while (true) {
      // 检查是否需要取消
      if (shouldCancelGeneration.value) {
        await reader.cancel()
        break
      }
      
      const { done, value } = await reader.read()
      
      if (done) {
        break
      }
      
      const chunk = decoder.decode(value, { stream: true })
      
      // 分割成多个事件
      const lines = chunk.split('\n')
      
      for (const line of lines) {
        if (line === '') continue
        if (line.startsWith(':')) continue
        
        try {
          const dataStr = line.replace(/^data: /, '')
          if (dataStr === '[DONE]') {
            break
          }
          
          const data = JSON.parse(dataStr)
          
          if (data.choices && data.choices[0] && data.choices[0].delta && data.choices[0].delta.content) {
            const content = data.choices[0].delta.content
            
            // 更新助手消息
            messages.value[assistantMessageId].content.text += content
            
            // 滚动到底部
            await nextTick()
            scrollToBottom()
          }
        } catch (error) {
          console.error('Error parsing chunk:', error)
        }
      }
    }
    
    // 流式输出完成
    if (messages.value[assistantMessageId]) {
      messages.value[assistantMessageId].streaming = false
    }
    
    // 检查是否被取消
    if (shouldCancelGeneration.value) {
      if (messages.value[assistantMessageId]) {
        messages.value[assistantMessageId].content.text += '\n\n[生成已取消]'
      }
      shouldCancelGeneration.value = false
    }
    
  } catch (error) {
    console.error('API call failed:', error)
    
    // 添加错误消息
    const errorMessage = {
      role: 'assistant',
      content: {
        text: `抱歉，API 调用失败：${error.message}`
      }
    }
    messages.value.push(errorMessage)
    
    // 滚动到底部
    await nextTick()
    scrollToBottom()
  } finally {
    isLoading.value = false
    isStreaming.value = false
    shouldCancelGeneration.value = false
  }
}
</script>

<style scoped>
.ai-assistant-page {
  min-height: 100vh;
  position: relative;
  z-index: 1;
}

.hero-section {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  position: relative;
}

.hero-content {
  text-align: center;
  max-width: 800px;
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

/* 聊天容器 */
.chat-container {
  max-width: 1000px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 25px;
  backdrop-filter: blur(15px);
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* 聊天消息区域 */
.chat-messages {
  height: 600px;
  overflow-y: auto;
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 消息样式 */
.message {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  max-width: 80%;
  animation: messageSlide 0.3s ease-out;
}

@keyframes messageSlide {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 用户消息 */
.message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

/* 助手消息 */
.message.assistant {
  align-self: flex-start;
}

.message.assistant .message-text {
  background: linear-gradient(135deg, rgba(118, 75, 162, 0.2), rgba(160, 96, 223, 0.2));
  border-color: rgba(118, 75, 162, 0.3);
  border-radius: 18px 18px 18px 5px;
  padding: 22px 26px;
  font-size: 1.05rem;
  line-height: 1.7;
  box-shadow: 0 8px 25px rgba(118, 75, 162, 0.2);
}

.message.assistant .message-text {
  color: rgba(255, 255, 255, 0.95);
}

.message.assistant .message-text::first-letter {
  font-size: 1.2em;
  font-weight: 600;
}

.message.assistant .message-text p {
  margin: 0 0 12px 0;
}

.message.assistant .message-text p:last-child {
  margin-bottom: 0;
}

.message.assistant .message-text ul,
.message.assistant .message-text ol {
  margin: 12px 0;
  padding-left: 24px;
}

.message.assistant .message-text li {
  margin: 6px 0;
}

/* 系统消息 */
.message.system-message {
  align-self: center;
  max-width: 90%;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 20px;
  padding: 20px;
}

.message.system-message .message-content {
  text-align: center;
}

/* 头像 */
.message-avatar {
  font-size: 2rem;
  flex-shrink: 0;
  margin-top: 5px;
}

/* 消息内容 */
.message-content {
  flex: 1;
}

/* 文本消息 */
.message-text {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 18px;
  padding: 18px 22px;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
  position: relative;
  overflow: hidden;
  font-size: 16px;
  font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
}

/* 流式输出动画 */
.message-text.streaming {
  position: relative;
}

.message-text.streaming::after {
  content: '';
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  width: 2px;
  height: 20px;
  background: #667eea;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0;
  }
}

.message.user .message-text {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
  border-color: rgba(102, 126, 234, 0.3);
}

/* 美化输出格式 */
.message-text p {
  margin: 0 0 12px 0;
  padding: 0;
}

.message-text p:last-child {
  margin-bottom: 0;
}

.message-text h1,
.message-text h2,
.message-text h3,
.message-text h4,
.message-text h5,
.message-text h6 {
  color: rgba(255, 255, 255, 0.95);
  margin: 16px 0 12px 0;
  font-weight: 600;
}

.message-text h1 {
  font-size: 24px;
}

.message-text h2 {
  font-size: 20px;
}

.message-text h3 {
  font-size: 18px;
}

.message-text h4 {
  font-size: 16px;
}

.message-text ul,
.message-text ol {
  margin: 12px 0;
  padding-left: 24px;
}

.message-text li {
  margin: 6px 0;
}

.message-text a {
  color: #667eea;
  text-decoration: none;
  transition: color 0.3s ease;
}

.message-text a:hover {
  color: #764ba2;
  text-decoration: underline;
}

.message-text code {
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 4px;
  padding: 2px 6px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 14px;
  color: #f093fb;
}

.message-text pre {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 16px;
  overflow-x: auto;
  margin: 12px 0;
}

.message-text pre code {
  background: none;
  border: none;
  padding: 0;
  color: rgba(255, 255, 255, 0.9);
}

.message-text blockquote {
  border-left: 4px solid #667eea;
  padding-left: 16px;
  margin: 12px 0;
  color: rgba(255, 255, 255, 0.7);
  font-style: italic;
}

.message-text hr {
  border: none;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin: 20px 0;
}

/* 图片消息 */
.message-image {
  margin-top: 10px;
  border-radius: 15px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.message-image img {
  max-width: 300px;
  max-height: 400px;
  border-radius: 15px;
}

/* 分析结果 */
.message-analysis {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
  margin-top: 10px;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
}

/* 加载动画 */
.loading-indicator {
  display: flex;
  gap: 10px;
  padding: 20px;
}

.loading-dot {
  width: 12px;
  height: 12px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  animation: loadingBounce 1.4s ease-in-out infinite;
}

.loading-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes loadingBounce {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

/* 聊天输入区域 */
.chat-input-area {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.02);
}

/* 顶部工具栏 */
.input-toolbar {
  margin-bottom: 15px;
}

.upload-buttons {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.btn-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
  border-color: #667eea;
  transform: translateY(-2px);
}

.btn-icon:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 模型选择部分 */
.model-selector {
  flex: 1;
  min-width: 200px;
}

.model-select {
  width: 100%;
  padding: 10px 14px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.model-select:focus {
  outline: none;
  border-color: #667eea;
  background: rgba(0, 0, 0, 0.6);
}

.model-select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 下拉菜单样式 */
.model-select option {
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 10px;
}

.model-select option:checked {
  background: rgba(102, 126, 234, 0.3);
}

.model-select option:hover {
  background: rgba(102, 126, 234, 0.2);
}

/* 文本输入部分 */
.text-input-section {
  margin-top: 10px;
}

.text-input-container {
  display: flex;
  gap: 12px;
  align-items: center;
}

.text-input {
  flex: 1;
  padding: 15px 20px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.text-input:focus {
  outline: none;
  border-color: #667eea;
  background: rgba(255, 255, 255, 0.1);
}

.text-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 按钮样式 */
.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  min-width: 100px;
  padding: 15px 30px;
  border-radius: 25px;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.btn-remove {
  position: absolute;
  top: -10px;
  right: -10px;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: #ff4757;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.btn-remove:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4);
}

.btn-remove:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* 功能特点部分 */
.features-section {
  background: rgba(255, 255, 255, 0.02);
  margin-top: 80px;
}

.features-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.feature-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 45px 35px;
  text-align: center;
  backdrop-filter: blur(10px);
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
  transition: left 0.6s ease;
}

.feature-card:hover::before {
  left: 100%;
}

.feature-card:hover {
  transform: translateY(-10px);
  border-color: rgba(102, 126, 234, 0.5);
  box-shadow: 0 20px 60px rgba(102, 126, 234, 0.2);
}

.feature-icon {
  font-size: 5rem;
  margin-bottom: 30px;
  filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.5));
}

.feature-card h3 {
  color: white;
  font-size: 1.6rem;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.feature-card p {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.7;
  font-size: 1.1rem;
}

/* 滚动条样式 */
.chat-messages::-webkit-scrollbar {
  width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #764ba2 0%, #f093fb 100%);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .title-main {
    font-size: 2.5rem;
  }
  
  .title-sub {
    font-size: 1rem;
    letter-spacing: 3px;
  }
  
  .chat-container {
    margin: 0 20px;
  }
  
  .chat-messages {
    height: 500px;
    padding: 20px;
  }
  
  .message {
    max-width: 95%;
  }
  
  .chat-input-area {
    padding: 15px;
  }
  
  .text-input-container {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  
  .upload-buttons {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  
  .model-selector {
    width: 100%;
  }
  
  .btn-primary {
    width: 100%;
  }
  
  .features-content {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>
