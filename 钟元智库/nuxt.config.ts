export default defineNuxtConfig({
  devtools: {
    enabled: false
  },
  modules: [
    '@nuxtjs/tailwindcss'
  ],
  css: [
    '@/assets/css/main.css'
  ],
  app: {
    head: {
      title: '钟元智库（数据知识产权）有限公司',
      meta: [
        {
          name: 'description',
          content: '钟元智库是一家专注于数据知识产权服务的专业机构，为企业提供全方位的数据知识产权保护解决方案。'
        }
      ]
    }
  },
  devServer: {
    port: 8888
  },
  telemetry: false
})