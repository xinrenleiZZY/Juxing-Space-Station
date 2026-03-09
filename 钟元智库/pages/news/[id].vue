<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-primary to-secondary text-white py-20 md:py-28">
      <div class="container mx-auto px-4">
        <h1 class="text-4xl md:text-5xl font-bold mb-6">
          新闻详情
        </h1>
        <p class="text-xl mb-8">
          了解行业最新动态和公司新闻
        </p>
      </div>
    </section>

    <!-- News Detail Section -->
    <section class="section bg-white">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto">
          <!-- News Meta -->
          <div class="mb-8">
            <span class="text-gray-600">发布时间：2026-02-20</span>
            <span class="mx-4 text-gray-400">|</span>
            <span class="text-primary">分类：行业动态</span>
          </div>

          <!-- News Content -->
          <div class="prose max-w-none">
            <h2 class="text-3xl font-bold mb-6">国家知识产权局发布数据知识产权保护新政策</h2>
            
            <p class="text-gray-600 mb-6">
              国家知识产权局近日发布了《数据知识产权保护条例》，进一步加强对数据知识产权的保护，为企业提供更加明确的法律依据。该条例将于2026年3月1日起正式实施。
            </p>

            <h3 class="text-2xl font-bold mb-4">条例主要内容</h3>
            <p class="text-gray-600 mb-4">
              新条例明确了数据知识产权的定义、范围和保护措施，为数据知识产权的登记、保护和维权提供了更加完善的制度保障。条例主要包括以下内容：
            </p>
            <ul class="list-disc list-inside space-y-2 mb-6 text-gray-600">
              <li>明确了数据知识产权的法律地位和保护范围</li>
              <li>建立了数据知识产权登记制度</li>
              <li>完善了数据知识产权保护措施</li>
              <li>加强了数据知识产权维权机制</li>
            </ul>

            <h3 class="text-2xl font-bold mb-4">对企业的影响</h3>
            <p class="text-gray-600 mb-4">
              新条例的实施将对企业产生重要影响。企业需要更加重视数据知识产权的保护，建立健全的数据知识产权管理体系。同时，条例也为企业提供了更加明确的法律依据，有助于企业更好地保护自己的数据资产。
            </p>
            <p class="text-gray-600 mb-6">
              钟元智库作为专业的数据知识产权服务机构，将密切关注条例的实施情况，为企业提供专业的数据知识产权保护服务。
            </p>

            <h3 class="text-2xl font-bold mb-4">钟元智库的服务</h3>
            <p class="text-gray-600 mb-4">
              钟元智库为企业提供全方位的数据知识产权服务，包括数据知识产权登记、保护、咨询和维权等。我们拥有专业的团队和丰富的经验，能够为企业提供高质量的服务。
            </p>
            <p class="text-gray-600 mb-6">
              如果您需要数据知识产权相关的服务，欢迎联系我们。我们将竭诚为您服务。
            </p>
          </div>

          <!-- Back Button -->
          <div class="mt-12">
            <a href="/news" class="btn-primary inline-block">
              返回新闻列表
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