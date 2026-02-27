<template>
  <div class="zyzk001-page">
    <!-- 第一层：标题 -->
    <div class="layer-title">
      <h1 class="title-text">钟元智库</h1>
    </div>
    
    <!-- 第二层：说明 -->
    <div class="layer-description">
      <div class="description-text">/ 操 作 简 单  高 效 快 捷 /</div>
    </div>
    
    <!-- 第三层：操作区 -->
    <div class="layer-operation">
      <!-- 左侧图片区（60%） -->
      <div class="image-section">
        <div class="image-placeholder">
          <div class="placeholder-content">
            <!-- <div class="placeholder-icon">📊</div>
            <div class="placeholder-text">钟元智库数据知识产权</div> -->
             <img src="/1.png" alt="钟元智库数据知识产权" class="main-image">

          </div>
        </div>
      </div>
      
      <!-- 右侧按钮区（40%） -->
      <div class="button-section">
        <button class="parallelogram-btn btn-left">办证申请</button>
        <button class="parallelogram-btn btn-right">联系我们</button>
        <button class="parallelogram-btn btn-left">公司公告</button>
        <button class="parallelogram-btn btn-right">证书查询</button>
      </div>
    </div>
  </div>
</template>

<script setup>
// 页面逻辑
</script>

<style scoped>
.zyzk001-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: rgba(10, 10, 30, 0.95);
  font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
  position: relative;
  z-index: 1;
  width: 100%;
}

/* 第一层：标题 */
.layer-title {
  flex: 0 0 auto;
  padding: 40px 20px;
  text-align: center;
  background: rgba(10, 10, 30, 0.98);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.title-text {
  font-size: 3rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.95);
  letter-spacing: 8px;
  margin: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 第二层：说明 */
.layer-description {
  flex: 0 0 auto;
  padding: 30px 20px;
  text-align: center;
  background: rgba(10, 10, 30, 0.96);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.description-text {
  font-size: 1.5rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  letter-spacing: 12px;
  margin: 0;
}

/* 第三层：操作区 */
.layer-operation {
  flex: 1;
  display: flex;
  padding: 40px 20px;
  gap: 40px;
  background: rgba(10, 10, 30, 0.95);
  width: 100%;
}

/* 左侧图片区（60%） */
.image-section {
  flex: 6;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 15px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.image-placeholder {
  width: 100%;
  height: 100%;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  border-radius: 10px;
  border: 2px dashed rgba(255, 255, 255, 0.2);
}

.placeholder-content {
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-icon {
  font-size: 5rem;
  margin-bottom: 20px;
}

.placeholder-text {
  font-size: 1.2rem;
  font-weight: 600;
  letter-spacing: 2px;
}

/* 主图片样式 */
.main-image {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  border-radius: 10px;
  object-fit: contain;
}

/* 右侧按钮区（40%） */
.button-section {
  flex: 4;
  display: flex;
  flex-direction: column;
  gap: 30px;
  justify-content: center;
  padding: 20px;
}

/* 平行四边形按钮 */
.parallelogram-btn {
  padding: 20px 40px;
  font-size: 1.3rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  transform: skewX(-10deg);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.parallelogram-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), transparent);
  border-radius: 5px;
}

.parallelogram-btn:hover {
  transform: skewX(-10deg) translateX(10px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

.parallelogram-btn:active {
  transform: skewX(-10deg) translateX(5px);
}

/* 按钮布局：1、3居左，2、4居右 */
.btn-left {
  align-self: flex-start;
  margin-left: 20px;
}

.btn-right {
  align-self: flex-end;
  margin-right: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .layer-operation {
    flex-direction: column;
    gap: 30px;
  }
  
  .image-section {
    flex: 1;
    min-height: 300px;
  }
  
  .button-section {
    flex: 1;
    gap: 20px;
  }
  
  .parallelogram-btn {
    padding: 15px 30px;
    font-size: 1.1rem;
  }
  
  .title-text {
    font-size: 2rem;
    letter-spacing: 4px;
  }
  
  .description-text {
    font-size: 1.2rem;
    letter-spacing: 6px;
  }
}
</style>