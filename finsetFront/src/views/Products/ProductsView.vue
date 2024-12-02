<template>
  <div class="finance-container">
    <!-- 상단 타이틀 섹션 -->
    <v-container fluid class="pt-16 pb-8">
      <v-row justify="center">
        <v-col cols="12" class="text-center">
          <h1 class="text-h3 font-weight-bold mb-2 gradient-text">
            금융상품 콕집기
          </h1>
          <p class="text-subtitle-1 text-medium-emphasis">
            <v-icon color="primary" class="pin-icon">mdi-pin</v-icon>
            찝어드리는 맞춤 금융상품
          </p>
        </v-col>
      </v-row>
    </v-container>
     <!-- 카테고리 선택 섹션 -->
     <v-container fluid class="pb-8">
      <v-row justify="center">
        <v-col cols="12" sm="8" md="6">
          <v-card elevation="0" color="transparent" class="rounded-xl">
            <v-card-text>
              <v-btn-toggle
                v-model="selectedCategory"
                mandatory
                class="d-flex justify-center custom-toggle"
              >
                <v-btn
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                  class="toggle-btn"
                  min-width="160"
                  height="48"
                >
                  <v-icon :icon="category.icon" class="mr-2"></v-icon>
                  {{ category.name }}
                </v-btn>
              </v-btn-toggle>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
<!-- 검색 섹션 -->
<v-container fluid class="pb-4">
  <v-row justify="center">
    <v-col cols="12" sm="8" md="6">
      <v-text-field
        v-model="searchQuery"
        label="상품명을 검색하세요"
        clearable
        variant="outlined"
        color="primary"
        class="search-bar"
        hide-details
      >
        <template v-slot:append>
          <v-icon color="primary">mdi-magnify</v-icon>
        </template>
      </v-text-field>
    </v-col>
  </v-row>
</v-container>
<v-container>
  <v-row>
    <v-col
      v-for="product in filteredProducts"
      :key="product.id"
      cols="12"
      sm="6"
      md="4"
      class="product-card-wrapper"
    >
      <v-hover v-slot="{ isHovering, props }">
        <v-card
          v-bind="props"
          :elevation="isHovering ? 8 : 2"
          :class="[ 'h-100 rounded-xl product-card', { 'on-hover': isHovering } ]"
        >
          <!-- 상품 카드 내용 -->
          <div class="card-highlight-border"></div>
              <v-card-item>
                <template v-slot:prepend>
                  <v-avatar
                    :color="isHovering ? 'primary-darken-1' : 'primary'"
                    size="48"
                    class="mr-4 avatar-transition"
                  >
                    <v-icon
                      :icon="selectedCategory === 'deposit' ? 'mdi-bank' : 'mdi-piggy-bank'"
                      color="white"
                      size="24"
                      class="icon-transition"
                    ></v-icon>
                  </v-avatar>
                </template>
                <v-card-title class="text-h6 mb-1">
                  {{ product.fin_prdt_nm }}
                </v-card-title>
                <v-card-subtitle>
                  {{ product.kor_co_nm }}
                </v-card-subtitle>
              </v-card-item>

              <v-card-text>
                <v-list v-if="product.options?.length" class="product-info-list rounded-lg">
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary" class="mr-2">mdi-calendar-month</v-icon>
                    </template>
                    <v-list-item-title class="d-flex justify-space-between">
                      <span>가입기간</span>
                      <span class="font-weight-medium">
                        {{ product.options[0].save_trm }}개월
                      </span>
                    </v-list-item-title>
                  </v-list-item>

                  <v-divider class="mx-4"></v-divider>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary" class="mr-2">mdi-percent</v-icon>
                    </template>
                    <v-list-item-title class="d-flex justify-space-between">
                      <span>기본금리</span>
                      <span class="text-primary font-weight-bold">
                        {{ product.options[0].intr_rate }}%
                      </span>
                    </v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-card-text>

              <v-card-actions class="pa-4">
                <v-btn
                  block
                  color="primary"
                  variant="elevated"
                  @click="goToDetail(product.id)"
                  class="detail-btn text-none rounded-lg"
                  height="48"
                >
                  상세정보 살펴보기
                  <v-icon class="ml-2 btn-icon">mdi-arrow-right</v-icon>
                </v-btn>
              </v-card-actions>
        </v-card>
      </v-hover>
    </v-col>
  </v-row>
</v-container>

<v-divider class="my-divider"></v-divider>

    <!-- 상품 목록 섹션 -->
    <v-container>
      <v-row>
        <v-col
          v-for="product in currentProducts"
          :key="product.id"
          cols="12"
          sm="6"
          md="4"
          class="product-card-wrapper"
        >
          <v-hover v-slot="{ isHovering, props }">
            <v-card
              v-bind="props"
              :elevation="isHovering ? 8 : 2"
              :class="[
                'h-100 rounded-xl product-card',
                { 'on-hover': isHovering }
              ]"
            >
              <div class="card-highlight-border"></div>
              <v-card-item>
                <template v-slot:prepend>
                  <v-avatar
                    :color="isHovering ? 'primary-darken-1' : 'primary'"
                    size="48"
                    class="mr-4 avatar-transition"
                  >
                    <v-icon
                      :icon="selectedCategory === 'deposit' ? 'mdi-bank' : 'mdi-piggy-bank'"
                      color="white"
                      size="24"
                      class="icon-transition"
                    ></v-icon>
                  </v-avatar>
                </template>
                <v-card-title class="text-h6 mb-1">
                  {{ product.fin_prdt_nm }}
                </v-card-title>
                <v-card-subtitle>
                  {{ product.kor_co_nm }}
                </v-card-subtitle>
              </v-card-item>

              <v-card-text>
                <v-list v-if="product.options?.length" class="product-info-list rounded-lg">
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary" class="mr-2">mdi-calendar-month</v-icon>
                    </template>
                    <v-list-item-title class="d-flex justify-space-between">
                      <span>가입기간</span>
                      <span class="font-weight-medium">
                        {{ product.options[0].save_trm }}개월
                      </span>
                    </v-list-item-title>
                  </v-list-item>

                  <v-divider class="mx-4"></v-divider>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary" class="mr-2">mdi-percent</v-icon>
                    </template>
                    <v-list-item-title class="d-flex justify-space-between">
                      <span>기본금리</span>
                      <span class="text-primary font-weight-bold">
                        {{ product.options[0].intr_rate }}%
                      </span>
                    </v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-card-text>

              <v-card-actions class="pa-4">
                <v-btn
                  block
                  color="primary"
                  variant="elevated"
                  @click="goToDetail(product.id)"
                  class="detail-btn text-none rounded-lg"
                  height="48"
                >
                  상세정보 살펴보기
                  <v-icon class="ml-2 btn-icon">mdi-arrow-right</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-hover>
        </v-col>
      </v-row>
    </v-container>

    <!-- 로딩 오버레이 -->
    <v-overlay :model-value="loading" class="align-center justify-center">
      <v-progress-circular color="primary" indeterminate size="64"></v-progress-circular>
    </v-overlay>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useFinanceStore } from '@/stores/finance';
import { useRouter } from 'vue-router';

const store = useFinanceStore();
const router = useRouter();
const loading = ref(false);

const searchQuery = ref(''); // 검색어를 저장할 ref 추가

const filteredProducts = computed(() => {
  // 검색어를 소문자로 변환하여 대소문자 구분 없이 검색
  const query = searchQuery.value.toLowerCase();
  return currentProducts.value.filter(product =>
    product.fin_prdt_nm.toLowerCase().includes(query)
  );
});


const categories = [
  { id: 'deposit', name: '예금상품', icon: 'mdi-bank' },
  { id: 'saving', name: '적금상품', icon: 'mdi-piggy-bank' }
];

const selectedCategory = ref(localStorage.getItem('selectedCategory') || 'deposit');
const depositsWithOptions = ref(JSON.parse(localStorage.getItem('depositsWithOptions') || '[]'));
const savingsWithOptions = ref(JSON.parse(localStorage.getItem('savingsWithOptions') || '[]'));

watch(selectedCategory, (newValue) => {
  localStorage.setItem('selectedCategory', newValue);
});

const currentProducts = computed(() => {
  return selectedCategory.value === 'deposit' ? depositsWithOptions.value : savingsWithOptions.value;
});

const fetchProducts = async () => {
  try {
    loading.value = true;
    
    if (depositsWithOptions.value.length === 0) {
      await store.getDeposits();
      const deposits = await Promise.all(
        store.deposits.map(async (deposit) => {
          const options = await store.getDepositOptions(deposit.id);
          return { ...deposit, options: options || [] };
        })
      );
      depositsWithOptions.value = deposits;
      localStorage.setItem('depositsWithOptions', JSON.stringify(deposits));
    }

    if (savingsWithOptions.value.length === 0) {
      await store.getSavings();
      const savings = await Promise.all(
        store.savings.map(async (saving) => {
          const options = await store.getSavingOptions(saving.id);
          return { ...saving, options: options || [] };
        })
      );
      savingsWithOptions.value = savings;
      localStorage.setItem('savingsWithOptions', JSON.stringify(savings));
    }
  } catch (error) {
    console.error('상품 데이터 불러오기 실패:', error);
  } finally {
    loading.value = false;
  }
};

const goToDetail = (productId) => {
  router.push({ name: 'product-detail', params: { id: productId } });
};

onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
.my-divider {
  height: 4px;
  background: linear-gradient(90deg, #0891b2, #0e7490);
  border-radius: 2px;
}


.finance-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f7ff 0%, #e6f0f9 100%);
}

.gradient-text {
  background: linear-gradient(45deg, #0891b2, #0e7490);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 2px 2px 4px rgba(8, 145, 178, 0.1);
}

.product-card-wrapper {
  transition: transform 0.3s ease;
}

.product-card {
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background-color: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(8, 145, 178, 0.1);
  overflow: hidden;
}

.card-highlight-border {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #0891b2, #0e7490);
  transform: scaleX(0);
  transition: transform 0.3s ease;
  transform-origin: left;
}

.product-card.on-hover {
  transform: translateY(-5px);
  border-color: rgba(8, 145, 178, 0.2);
}

.product-card.on-hover .card-highlight-border {
  transform: scaleX(1);
}

.pin-icon {
  animation: pinAnimation 2s infinite;
  transform-origin: center;
}

@keyframes pinAnimation {
  0%, 100% {
    transform: translateY(0) rotate(0);
  }
  25% {
    transform: translateY(-3px) rotate(-5deg);
  }
  75% {
    transform: translateY(-3px) rotate(5deg);
  }
}

.custom-toggle {
  background: white;
  border-radius: 12px;
  padding: 4px;
  box-shadow: 0 2px 8px rgba(8, 145, 178, 0.1);
}

.toggle-btn {
  position: relative;
  transition: all 0.3s ease;
  color: #64748b !important;
  border: none !important;
  overflow: visible !important;
}

.toggle-btn:hover {
  color: #0891b2 !important;
}

.custom-toggle .v-btn--active {
  background: linear-gradient(135deg, #0891b2, #0e7490) !important;
  color: white !important;
  font-weight: 600;
}

.custom-toggle .v-btn--active:hover {
  color: white !important;
}

.product-info-list {
  background: #f8fafc !important;
  border: 1px solid rgba(8, 145, 178, 0.1);
}

.detail-btn {
  position: relative;
  transition: all 0.3s ease !important;
}

.detail-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(8, 145, 178, 0.3) !important;
}

.btn-icon {
  transition: transform 0.3s ease;
}

.detail-btn:hover .btn-icon {
  transform: translateX(4px);
}

.avatar-transition {
  transition: all 0.3s ease;
}

.icon-transition {
  transition: transform 0.3s ease;
}

.product-card.on-hover .icon-transition {
  transform: scale(1.1);
}

:deep(.v-card-title) {
  line-height: 1.5;
  font-size: 1.25rem;
  color: #1e293b;
}

:deep(.v-list-item) {
  min-height: 48px;
}

:deep(.v-container) {
  max-width: 1200px;
}
</style>