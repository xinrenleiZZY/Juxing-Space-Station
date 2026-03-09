<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-primary to-secondary text-white py-20 md:py-28">
      <div class="container mx-auto px-4">
        <h1 class="text-4xl md:text-5xl font-bold mb-6">
          案例详情
        </h1>
        <p class="text-xl mb-8">
          了解我们的成功案例
        </p>
      </div>
    </section>

    <!-- Case Detail Section -->
    <section class="section bg-white">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto">
          <!-- Case Image -->
          <div class="rounded-lg overflow-hidden shadow-lg mb-8">
            <img src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=business%20case%20study&image_size=landscape_16_9" alt="案例图片" class="w-full h-auto">
          </div>

          <!-- Case Info -->
          <div class="mb-8">
            <h2 class="text-3xl font-bold mb-4">某科技公司数据知识产权保护项目</h2>
            <div class="flex items-center mb-6">
              <span class="text-gray-600">项目时间：2025年3月 - 2025年6月</span>
              <span class="mx-4 text-gray-400">|</span>
              <span class="text-primary">项目类型：数据知识产权保护</span>
            </div>
          </div>

          <!-- Case Description -->
          <div class="mb-8">
            <h3 class="text-2xl font-bold mb-4">项目背景</h3>
            <p class="text-gray-600 mb-4">
              某科技公司是一家专注于人工智能和大数据分析的创新企业，拥有大量的数据资产。随着业务的发展，公司意识到数据知识产权保护的重要性，需要专业的服务来保护其数据资产。
            </p>
            <p class="text-gray-600">
              钟元智库为该公司提供了全面的数据知识产权保护服务，帮助其建立了完善的数据知识产权管理体系。
            </p>
          </div>

          <!-- Case Solution -->
          <div class="mb-8">
            <h3 class="text-2xl font-bold mb-4">解决方案</h3>
            <ul class="space-y-3">
              <li class="flex items-start">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary mr-2 mt-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span class="text-gray-600">数据知识产权登记服务</span>
              </li>
              <li class="flex items-start">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary mr-2 mt-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span class="text-gray-600">数据知识产权保护方案设计</span>
              </li>
              <li class="flex items-start">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary mr-2 mt-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span class="text-gray-600">数据知识产权培训服务</span>
              </li>
              <li class="flex items-start">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary mr-2 mt-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span class="text-gray-600">数据知识产权维权服务</span>
              </li>
            </ul>
          </div>

          <!-- Case Result -->
          <div class="mb-8">
            <h3 class="text-2xl font-bold mb-4">项目成果</h3>
            <p class="text-gray-600 mb-4">
              通过钟元智库的专业服务，该公司成功建立了完善的数据知识产权管理体系，有效保护了其数据资产。项目实施后，公司的数据知识产权得到了全面保护，为业务发展提供了有力保障。
            </p>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="bg-gray-50 p-6 rounded-lg text-center">
                <div class="text-3xl font-bold text-primary mb-2">50+</div>
                <div class="text-gray-600">登记数据知识产权</div>
              </div>
              <div class="bg-gray-50 p-6 rounded-lg text-center">
                <div class="text-3xl font-bold text-primary mb-2">100%</div>
                <div class="text-gray-600">保护成功率</div>
              </div>
              <div class="bg-gray-50 p-6 rounded-lg text-center">
                <div class="text-3xl font-bold text-primary mb-2">3个月</div>
                <div class="text-gray-600">项目周期</div>
              </div>
            </div>
          </div>

          <!-- Back Button -->
          <div class="mt-12">
            <a href="/case" class="btn-primary inline-block">
              返回案例列表
            </a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const route = useRoute()
</script>