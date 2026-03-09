<template>
  <div class="ai-chat-container">
    <!-- 标题栏 -->
    <div class="chat-header">
      <h1>AI智能对话</h1>
      <p>基于AI模型的智能助手</p>
    </div>

    <!-- 模型选择 -->
    <div class="model-selection">
      <label>选择模型：</label>
      <select v-model="selectedModelId" class="model-select">
        <option v-for="model in models" :key="model.id" :value="model.id">
          {{ model.name }}
        </option>
      </select>
    </div>

    <!-- 对话内容区域 -->
    <div class="chat-messages" ref="messagesContainer">
      <!-- 系统消息 -->
      <div class="message system-message">
        <div class="message-content">
          <p>👋 你好！我是AI智能助手。我可以帮你解答各种问题，包括：</p>
          <ul>
            <li>数据知识产权评估相关问题</li>
            <li>技术咨询和代码问题</li>
            <li>数据分析和处理建议</li>
            <li>其他专业问题</li>
          </ul>
          <p>请在下方输入你的问题，我会尽力为你提供专业的回答。</p>
        </div>
      </div>

      <!-- 用户消息 -->
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role === 'user' ? 'user-message' : 'assistant-message']">
        <div class="message-header">
          {{ msg.role === 'user' ? '你' : 'AI助手' }}
        </div>
        <div class="message-content" v-if="msg.role === 'user'">
          {{ msg.content }}
        </div>
        <div class="message-content" v-else v-html="msg.renderedContent"></div>
      </div>

      <!-- 加载中消息 -->
      <div v-if="isLoading" class="message assistant-message">
        <div class="message-header">AI助手</div>
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
      <textarea 
        v-model="userQuestion" 
        placeholder="请输入你的问题..." 
        class="chat-input"
        @keyup.enter.exact="sendQuestion"
        @keyup.enter.shift="$event.preventDefault()"
        :disabled="isLoading"
      ></textarea>
      <button 
        @click="sendQuestion" 
        class="send-button"
        :disabled="isLoading || !userQuestion.trim()"
      >
        发送
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
// 推荐安装：npm install marked （用于解析 Markdown）
import { marked } from 'marked'

// 你的模型列表
const models = ref([
  { id: 'doubao-1-5-vision-pro-32k-250115', name: '豆包 1.5 视觉 Pro 32k' },
  { id: 'doubao-1-5-lite-32k-250115', name: '豆包 1.5 Lite 32k' },
  { id: 'doubao-1-5-pro-32k-250115', name: '豆包 1.5 Pro 32k' },
  { id: 'doubao-seed-1-8-251228', name: '豆包种子 1.8' },
  { id: 'doubao-seed-1-6-lite-251015', name: '豆包种子 1.6 Lite' },
  { id: 'doubao-seed-1-6-vision-250815', name: '豆包种子 1.6 视觉' },
  { id: 'doubao-seed-1-6-251015', name: '豆包种子 1.6' },
  { id: 'doubao-seed-1-6-flash-250828', name: '豆包种子 1.6 Flash' },
  { id: 'deepseek-v3-2-251201', name: 'DeepSeek V3.2' },
  { id: 'deepseek-v3-1-terminus', name: 'DeepSeek V3.1' },
  { id: 'deepseek-r1-250528', name: 'DeepSeek R1' },
  { id: 'deepseek-v3-250324', name: 'DeepSeek V3' },
  { id: 'kimi-k2-thinking-251104', name: 'Kimi K2' },
  { id: 'glm-4-7-251222', name: 'GLM 4.7' }
])

// 响应式数据
const selectedModelId = ref(models.value[0].id) // 默认选第一个模型
const userQuestion = ref('')
const messages = ref([])
const isLoading = ref(false)
const messagesContainer = ref(null)
const apiKey = ref('a3e3e754-162c-4bf3-b9b6-7519784e4f00')

// 发送问题并获取格式化回答
const sendQuestion = async () => {
  if (!userQuestion.value.trim()) return

  // 添加用户消息
  const question = userQuestion.value.trim()
  messages.value.push({
    role: 'user',
    content: question
  })
  userQuestion.value = ''
  
  // 滚动到底部
  await nextTick()
  scrollToBottom()
  
  // 显示加载状态
  isLoading.value = true

  try {
    // 1. 配置请求参数
    const requestData = {
      model: selectedModelId.value, // 选中的模型ID
      messages: [
        // 系统提示：强制返回美观的 Markdown 格式
        {
          role: 'system',
          content: '你是一个专业的助手，回答必须使用清晰规范的 Markdown 格式：分段用换行，标题用 # 层级，列表用 - 或 1.，代码用 ``` 包裹，重点内容用 ** 加粗，不要多余符号，确保输出能直接渲染。'
        },
        // 用户的问题
        {
          role: 'user',
          content: question
        }
      ],
      temperature: 0.7, // 随机性，0-1 之间
      stream: false // 非流式返回
    }

    // 2. 调用 API - 这里使用正确的API地址
    const apiUrl = getApiUrl(selectedModelId.value)
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey.value}`
      },
      body: JSON.stringify(requestData)
    })

    // 3. 处理返回结果
    if (!response.ok) {
      throw new Error(`API请求失败: ${response.status} ${response.statusText}`)
    }
    
    const data = await response.json()
    console.log('API响应:', data)
    
    if (data.choices && data.choices[0]) {
      const answer = data.choices[0].message.content
      // 用 marked 解析 Markdown 成 HTML
      const renderedContent = marked.parse(answer)
      
      // 添加AI回复
      messages.value.push({
        role: 'assistant',
        content: answer,
        renderedContent: renderedContent
      })
    } else {
      throw new Error('API返回格式错误')
    }
  } catch (error) {
    console.error('API调用失败：', error)
    // 添加错误消息
    messages.value.push({
      role: 'assistant',
      content: `抱歉，回答获取失败：${error.message}`,
      renderedContent: `<p>抱歉，回答获取失败：${error.message}</p>`
    })
  } finally {
    isLoading.value = false
    // 滚动到底部
    await nextTick()
    scrollToBottom()
  }
}

// 根据模型ID获取对应的API地址
const getApiUrl = (modelId) => {
  // 这里根据模型类型返回不同的API地址
  // 注意：不同的模型可能需要不同的API端点
  if (modelId.includes('deepseek')) {
    return 'https://api.deepseek.com/v1/chat/completions'
  } else if (modelId.includes('doubao')) {
    return 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'
  } else if (modelId.includes('kimi')) {
    return 'https://api.moonshot.cn/v1/chat/completions'
  } else if (modelId.includes('glm')) {
    return 'https://open.bigmodel.cn/api/messages'
  } else {
    return 'https://api.deepseek.com/v1/chat/completions'
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 组件挂载时初始化
onMounted(() => {
  // 可以在这里初始化一些数据
})
</script>

<style scoped>
.ai-chat-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  display: flex;
  flex-direction: column;
  font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
}

.chat-header {
  background: rgba(255, 255, 255, 0.05);
  padding: 30px 20px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.chat-header h1 {
  color: #eaeaea;
  font-size: 2rem;
  margin: 0 0 10px 0;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.chat-header p {
  color: #a0aec0;
  font-size: 1rem;
  margin: 0;
}

.model-selection {
  background: rgba(255, 255, 255, 0.03);
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 10px;
}

.model-selection label {
  color: #eaeaea;
  font-size: 1rem;
  font-weight: 500;
}

.model-select {
  flex: 1;
  max-width: 400px;
  padding: 10px 15px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  color: #eaeaea;
  font-size: 1rem;
  cursor: pointer;
}

.model-select:focus {
  outline: none;
  border-color: #667eea;
}

.chat-messages {
  flex: 1;
  padding: 30px 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message {
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

.user-message {
  align-self: flex-end;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 18px 18px 4px 18px;
  color: white;
}

.assistant-message {
  align-self: flex-start;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 18px 18px 18px 4px;
  color: #eaeaea;
}

.system-message {
  align-self: center;
  max-width: 90%;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 18px;
  color: #eaeaea;
  text-align: center;
}

.message-header {
  font-size: 0.85rem;
  margin: 10px 15px 5px 15px;
  opacity: 0.8;
}

.message-content {
  padding: 15px;
  line-height: 1.6;
}

.message-content h1, .message-content h2, .message-content h3 {
  margin: 10px 0;
  color: inherit;
}

.message-content h1 {
  font-size: 1.3rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 5px;
}

.message-content h2 {
  font-size: 1.1rem;
}

.message-content h3 {
  font-size: 1rem;
}

.message-content p {
  margin: 8px 0;
}

.message-content ul, .message-content ol {
  margin: 8px 0 8px 20px;
}

.message-content li {
  margin: 4px 0;
}

.message-content code {
  background: rgba(0, 0, 0, 0.3);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Consolas', monospace;
  font-size: 0.9em;
}

.message-content pre {
  background: rgba(0, 0, 0, 0.3);
  padding: 15px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 10px 0;
}

.message-content pre code {
  background: transparent;
  padding: 0;
}

.message-content blockquote {
  border-left: 3px solid #667eea;
  margin: 10px 0;
  padding-left: 15px;
  color: rgba(255, 255, 255, 0.8);
}

.loading-indicator {
  display: flex;
  gap: 8px;
  justify-content: center;
  padding: 10px 0;
}

.loading-dot {
  width: 10px;
  height: 10px;
  background: #667eea;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.loading-dot:nth-child(1) { animation-delay: -0.32s; }
.loading-dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.chat-input-area {
  background: rgba(255, 255, 255, 0.03);
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  gap: 15px;
  align-items: flex-end;
}

.chat-input {
  flex: 1;
  min-height: 80px;
  max-height: 200px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  color: #eaeaea;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  line-height: 1.4;
}

.chat-input:focus {
  outline: none;
  border-color: #667eea;
}

.chat-input::placeholder {
  color: #6b7280;
}

.send-button {
  padding: 15px 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* 滚动条样式 */
.chat-messages::-webkit-scrollbar {
  width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.5);
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.8);
}
</style>