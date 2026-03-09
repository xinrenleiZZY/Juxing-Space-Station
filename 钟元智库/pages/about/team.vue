<template>
  <div>
    <h1>团队页面</h1>
  </div>
</template>

<script>
export default {
  name: 'TeamPage'
}
</script><template>
  <div>Team Page</div>
</template><template>
  <div>团队页面</div>
</template><template>
  <div class="team-page">
    <h1>专家团队</h1>
    <p>钟元智库专业团队</p>
  </div>
</template>

<script setup>
// 团队页面组件
</script>

<style scoped>
.team-page {
  padding: 40px;
  text-align: center;
}

h1 {
  color: white;
  font-size: 2rem;
  margin-bottom: 20px;
}

p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
}
</style><template>
  <div>Team Page</div>
</template><template>
  <div>
    <h1>团队页面</h1>
  </div>
</template>

<script>
export default {
  name: 'TeamPage'
}
</script><template>
  <div>团队页面</div>
</template><template>
  <div class="team-page">
    <h1>专家团队</h1>
    <p>钟元智库专业团队</p>
  </div>
</template>

<script setup>
// 团队页面组件
</script>

<style scoped>
.team-page {
  padding: 40px;
  text-align: center;
}

h1 {
  color: white;
  font-size: 2rem;
  margin-bottom: 20px;
}

p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
}
</style><template>
  <div class="team-page">
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="title-main">专家团队</span>
          <span class="title-sub">Expert Team</span>
        </h1>
        <p class="hero-description">
          钟元智库拥有一支专业的数据知识产权评估团队<br>
          为企业提供全方位的数据分析和知识产权保护服务
        </p>
      </div>
    </section>

    <section class="team-section">
      <div class="section-header">
        <h2 class="section-title">我们的专家</h2>
        <div class="section-line"></div>
      </div>
      
      <div class="team-container">
        <div class="team-grid">
          <!-- 团队成员卡片 -->
          <div class="team-card">
            <div class="team-avatar">
              <div class="avatar-placeholder">👤</div>
            </div>
            <h3 class="team-name">张教授</h3>
            <p class="team-title">数据知识产权专家</p>
            <p class="team-desc">
              拥有10年以上数据知识产权评估经验，专注于数据价值分析和确权认证
            </p>
          </div>
          
          <div class="team-card">
            <div class="team-avatar">
              <div class="avatar-placeholder">👤</div>
            </div>
            <h3 class="team-name">李博士</h3>
            <p class="team-title">数据分析专家</p>
            <p class="team-desc">
              数据科学博士，擅长数据质量评估和特征工程，为企业提供数据优化方案
            </p>
          </div>
          
          <div class="team-card">
            <div class="team-avatar">
              <div class="avatar-placeholder">👤</div>
            </div>
            <h3 class="team-name">王律师</h3>
            <p class="team-title">知识产权律师</p>
            <p class="team-desc">
              专注于数据知识产权法律事务，为企业提供合规性评估和法律建议
            </p>
          </div>
          
          <div class="team-card">
            <div class="team-avatar">
              <div class="avatar-placeholder">👤</div>
            </div>
            <h3 class="team-name">陈工程师</h3>
            <p class="team-title">数据技术专家</p>
            <p class="team-desc">
              资深数据工程师，专注于数据清洗、脱敏和安全处理技术
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.team-page {
  min-height: 100vh;
  position: relative;
  z-index: 1;
}

.hero-section {
  min-height: 40vh;
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
  margin-bottom: 20px;
}

.title-main {
  display: block;
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 10px;
}

.title-sub {
  display: block;
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.7);
  letter-spacing: 4px;
  text-transform: uppercase;
}

.hero-description {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
}

.team-section {
  padding: 60px 20px;
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
}

.section-title {
  font-size: 2rem;
  color: white;
  margin-bottom: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-line {
  width: 80px;
  height: 3px;
  background: linear-gradient(90deg, transparent, #667eea, transparent);
  margin: 0 auto;
}

.team-container {
  max-width: 1200px;
  margin: 0 auto;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.team-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(15px);
}

.team-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 60px rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.3);
}

.team-avatar {
  margin-bottom: 20px;
}

.avatar-placeholder {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  margin: 0 auto;
}

.team-name {
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 8px;
  font-weight: 600;
}

.team-title {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 15px;
}

.team-desc {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
}

@media (max-width: 768px) {
  .title-main {
    font-size: 2rem;
  }
  
  .team-grid {
    grid-template-columns: 1fr;
  }
}
</style>