<template>
  <div class="main-container bg-[#e7f0f7]">
    <header class="fixed w-full bg-white/80 backdrop-blur-md z-50 border-b border-teal-100">
      <nav class="container mx-auto flex justify-between items-center p-4">
        <div class="nav-links flex items-center space-x-8">
          <RouterLink :to="{name:'products'}" class="nav-link group">
            <Search class="w-5 h-5 text-gray-500 group-hover:text-teal-500" />
            <span>상품조회</span>
          </RouterLink>
    
          <RouterLink :to="{name :'chatbot'}" class="nav-link group">
            <Bot class="w-5 h-5 text-gray-500 group-hover:text-teal-500" />
            <span>AI 상품 추천</span>
          </RouterLink>
          
          <RouterLink :to="{name :'searchMap'}" class="nav-link group">
            <MapPinned class="w-5 h-5 text-gray-500 group-hover:text-teal-500" />
            <span>위치</span>
          </RouterLink>

          <RouterLink :to="{name :'exchanges'}" class="nav-link group">
            <DollarSign class="w-5 h-5 text-gray-500 group-hover:text-teal-500" />
            <span>환율</span>
          </RouterLink>
        </div>
      </nav>
    </header>

    <section class="slide-section min-h-screen pt-24">
      <div class="container mx-auto relative">
        <div 
          class="tweezers-container"
          :style="{ transform: `rotate(${tweezersRotation}deg)` }"
        >
          <img src="/push-pin.png" alt="핀셋" class="tweezers" />
        </div>

        <transition-group 
          name="slide" 
          tag="div" 
          class="slides-wrapper"
        >
          <div 
            v-for="(slide, index) in slides" 
            :key="slide.id"
            v-show="currentSlide === index"
            class="slide-card"
            :class="{ 'being-picked': isPickingSlide }"
            style="background-color: #e7f0f9;"
          >
            <div class="grid grid-cols-2 gap-8 items-center">
              <div class="slide-content p-8">
                <h2 class="text-4xl font-bold mb-6">
                  <span class="text-teal-500">{{ slide.highlight }}</span>
                  {{ slide.title }}
                </h2>
                <p class="text-xl text-gray-600 mb-8">{{ slide.description }}</p>
              </div>
              <div class="slide-image relative">
                <img :src="slide.image" :alt="slide.title" class="w-full rounded-xl shadow-lg" />
                <div class="absolute -top-4 -right-4 bg-white p-3 rounded-lg shadow-lg">
                </div>
              </div>
            </div>
          </div>
        </transition-group>

        <div class="slide-nav flex gap-4 justify-center mt-8">
          <button 
            v-for="(slide, index) in slides" 
            :key="'nav-' + slide.id"
            @click="goToSlide(index)"
            class="slide-nav-dot"
            :class="{ 'active': currentSlide === index }"
          />
        </div>
      </div>
    </section>

    <footer class=" mt-16">
      <div class="container mx-auto py-8 px-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 class="text-lg font-semibold text-gray-800 mb-4">About Us</h3>
            <p class="text-gray-600">
              금융 상품 추천 서비스를 제공하여 고객님의 더 나은 금융 생활을 돕습니다.
            </p>
          </div>
      
          <div>
            <h3 class="text-lg font-semibold text-gray-800 mb-4">Contact</h3>
            <address class="text-gray-600 not-italic">
              <p>광주광역시 광산구 장덕로</p>
              <p>Email: support@finset.com</p>
              <p>Tel: (062) 1234-5678</p>
            </address>
          </div>
        </div>
        <div class="border-t border-gray-200 mt-8 pt-8 text-center text-gray-600">
          <p>&copy; 2024 Finset. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { Search, MapPinned, DollarSign, Bot } from 'lucide-vue-next'
import { RouterLink } from 'vue-router'

const currentSlide = ref(0)
const isPickingSlide = ref(false)
const tweezersRotation = ref(0)
let autoSlideInterval = null

const slides = [
  {
    id: 1,
    highlight: '정확한',
    title: '금융 상품 추천',
    description: 'AI 기반 분석으로 당신의 상황에 꼭 맞는 금융 상품을 찾아드립니다.',
    image: '/analysis.png'
  },
  {
    id: 2,
    highlight: '스마트한',
    title: '환율 계산',
    description: '실시간 시장 환율을 통해서 환율 정보를 알려드립니다.',
    image:'/exchange.png'
  },
  {
    id: 3,
    highlight: '내주변',
    title: '은행 위치 찾기',
    description: '위치 주변 은행의 위치 정보를 알려드립니다.',
    image: '/bank.png'
  }
]

const goToSlide = async (index) => {
  if (currentSlide.value === index) return
  
  isPickingSlide.value = true
  tweezersRotation.value = -25
  
  await new Promise(resolve => setTimeout(resolve, 500))
  currentSlide.value = index
  tweezersRotation.value = 0
  
  await new Promise(resolve => setTimeout(resolve, 500))
  isPickingSlide.value = false
}

const startAutoSlide = () => {
  autoSlideInterval = setInterval(() => {
    const nextSlide = (currentSlide.value + 1) % slides.length
    goToSlide(nextSlide)
  }, 5000)
}

onMounted(() => {
  startAutoSlide()
})

onBeforeUnmount(() => {
  if (autoSlideInterval) {
    clearInterval(autoSlideInterval)
  }
})
</script>

<style scoped>
.nav-link {
  @apply flex flex-col items-center gap-1 text-sm text-gray-500 hover:text-teal-500 transition-colors;
}

.slide-section {
  perspective: 1000px;
}

.tweezers-container {
  position: absolute;
  top: -30px;
  right: 80px;
  z-index: 50;
  transition: transform 0.5s ease;
  transform-origin: top right;
}

.tweezers {
  width: 50px;
  height: auto;
}

.slides-wrapper {
  position: relative;
  transform-style: preserve-3d;
}

.slide-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.5s ease;
  transform-origin: top right;
}

.being-picked {
  transform: translateY(-20px) rotate(-3deg);
  opacity: 0.8;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.5s ease;
}

.slide-enter-from {
  transform: translateX(100%) rotate(5deg);
  opacity: 0;
}

.slide-leave-to {
  transform: translateX(-100%) rotate(-5deg);
  opacity: 0;
}

.slide-nav-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #e2e8f0;
  transition: all 0.3s ease;
}

.slide-nav-dot.active {
  width: 32px;
  border-radius: 6px;
  background-color: #14b8a6;
}
</style>