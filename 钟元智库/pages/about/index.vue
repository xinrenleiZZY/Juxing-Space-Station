<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-primary to-secondary text-white py-20 md:py-28">
      <div class="container mx-auto px-4">
        <h1 class="text-4xl md:text-5xl font-bold mb-6">关于我们</h1>
        <p class="text-xl mb-8">
          钟元智库（数据知识产权）有限公司，专注于数据知识产权服务
        </p>
      </div>
    </section>

    <!-- Company Introduction Section -->
    <section class="section bg-white">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row items-center gap-12">
          <div class="md:w-1/2">
            <h2 class="section-title">公司简介</h2>
            <p class="text-gray-600 mb-6">
              钟元智库（数据知识产权）有限公司成立于2020年，是一家专注于数据知识产权服务的专业机构。我们拥有一支经验丰富的专业团队，为企业提供全方位的数据知识产权保护解决方案。
            </p>
            <p class="text-gray-600 mb-8">
              我们的使命是通过专业的服务，帮助企业保护和利用数据知识产权，促进数字经济的健康发展。我们致力于成为数据知识产权领域的领导者，为客户创造最大价值。
            </p>
          </div>
          <div class="md:w-1/2">
            <div class="rounded-lg overflow-hidden shadow-lg">
              <img src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=modern%20business%20team%20meeting&image_size=landscape_16_9" alt="公司团队" class="w-full h-auto">
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Mission Vision Section -->
    <section class="section bg-gray-50">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="card">
            <h3 class="text-2xl font-bold mb-4">我们的使命</h3>
            <p class="text-gray-600">
              通过专业的服务，帮助企业保护和利用数据知识产权，促进数字经济的健康发展。
            </p>
          </div>
          <div class="card">
            <h3 class="text-2xl font-bold mb-4">我们的愿景</h3>
            <p class="text-gray-600">
              成为数据知识产权领域的领导者，为客户创造最大价值。
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Team Section -->
    <section class="section bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="section-title">我们的团队</h2>
          <p class="section-subtitle">
            专业的团队，为您提供最优质的服务
          </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="card text-center">
            <div class="w-32 h-32 bg-gray-300 rounded-full mx-auto mb-4 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-500" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
            </div>
            <h4 class="text-xl font-bold mb-2">张博士</h4>
            <p class="text-gray-600 mb-4">创始人 & CEO</p>
            <p class="text-gray-600">
              拥有10年数据知识产权领域经验，曾在多家知名企业担任知识产权顾问。
            </p>
          </div>
          <div class="card text-center">
            <div class="w-32 h-32 bg-gray-300 rounded-full mx-auto mb-4 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-500" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
            </div>
            <h4 class="text-xl font-bold mb-2">李律师</h4>
            <p class="text-gray-600 mb-4">知识产权律师</p>
            <p class="text-gray-600">
              拥有丰富的知识产权诉讼经验，专注于数据知识产权领域的法律事务。
            </p>
          </div>
          <div class="card text-center">
            <div class="w-32 h-32 bg-gray-300 rounded-full mx-auto mb-4 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-500" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
            </div>
            <h4 class="text-xl font-bold mb-2">王分析师</h4>
            <p class="text-gray-600 mb-4">数据分析师</p>
            <p class="text-gray-600">
              拥有丰富的数据分析经验，专注于数据价值评估和数据挖掘。
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Development History Section -->
    <section class="section bg-gray-50">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="section-title">发展历程</h2>
          <p class="section-subtitle">
            我们的成长故事
          </p>
        </div>
        <div class="relative">
          <!-- Timeline -->
          <div class="absolute left-1/2 transform -translate-x-1/2 h-full w-1 bg-primary"></div>
          
          <!-- Timeline Items -->
          <div class="space-y-12">
            <div class="flex flex-col md:flex-row items-center">
              <div class="md:w-1/2 md:pr-12 md:text-right mb-6 md:mb-0">
                <h3 class="text-2xl font-bold mb-2">2020年</h3>
                <p class="text-gray-600">
                  钟元智库（数据知识产权）有限公司正式成立，专注于数据知识产权服务。
                </p>
              </div>
              <div class="z-10 w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                <span class="text-white font-bold">1</span>
              </div>
              <div class="md:w-1/2 md:pl-12"></div>
            </div>
            
            <div class="flex flex-col md:flex-row items-center">
              <div class="md:w-1/2 md:pr-12"></div>
              <div class="z-10 w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                <span class="text-white font-bold">2</span>
              </div>
              <div class="md:w-1/2 md:pl-12 mb-6 md:mb-0">
                <h3 class="text-2xl font-bold mb-2">2021年</h3>
                <p class="text-gray-600">
                  获得国家知识产权局认证，成为数据知识产权服务领域的专业机构。
                </p>
              </div>
            </div>
            
            <div class="flex flex-col md:flex-row items-center">
              <div class="md:w-1/2 md:pr-12 md:text-right mb-6 md:mb-0">
                <h3 class="text-2xl font-bold mb-2">2022年</h3>
                <p class="text-gray-600">
                  服务客户超过100家，成为行业内知名的数据知识产权服务提供商。
                </p>
              </div>
              <div class="z-10 w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                <span class="text-white font-bold">3</span>
              </div>
              <div class="md:w-1/2 md:pl-12"></div>
            </div>
            
            <div class="flex flex-col md:flex-row items-center">
              <div class="md:w-1/2 md:pr-12"></div>
              <div class="z-10 w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                <span class="text-white font-bold">4</span>
              </div>
              <div class="md:w-1/2 md:pl-12 mb-6 md:mb-0">
                <h3 class="text-2xl font-bold mb-2">2023年</h3>
                <p class="text-gray-600">
                  推出数据知识产权保护平台，为客户提供更加便捷的服务。
                </p>
              </div>
            </div>
            
            <div class="flex flex-col md:flex-row items-center">
              <div class="md:w-1/2 md:pr-12 md:text-right mb-6 md:mb-0">
                <h3 class="text-2xl font-bold mb-2">2024年</h3>
                <p class="text-gray-600">
                  扩大业务范围，提供更加全面的数据知识产权解决方案。
                </p>
              </div>
              <div class="z-10 w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                <span class="text-white font-bold">5</span>
              </div>
              <div class="md:w-1/2 md:pl-12"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Certifications Section -->
    <section class="section bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="section-title">资质证书</h2>
          <p class="section-subtitle">
            我们的专业认证
          </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="card">
            <h3 class="text-xl font-bold mb-4">国家知识产权局认证</h3>
            <p class="text-gray-600 mb-4">
              获得国家知识产权局颁发的知识产权服务机构认证。
            </p>
            <div class="bg-gray-100 p-4 rounded-md">
              <p class="text-center text-gray-500">证书编号：1234567890</p>
              <p class="text-center text-gray-500">有效期至：2027年12月31日</p>
            </div>
          </div>
          <div class="card">
            <h3 class="text-xl font-bold mb-4">ISO 9001质量管理体系认证</h3>
            <p class="text-gray-600 mb-4">
              获得ISO 9001质量管理体系认证，确保服务质量。
            </p>
            <div class="bg-gray-100 p-4 rounded-md">
              <p class="text-center text-gray-500">证书编号：ISO9001-2024-001</p>
              <p class="text-center text-gray-500">有效期至：2027年12月31日</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
