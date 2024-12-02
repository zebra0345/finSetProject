<template>
  <div class="product-detail">
    <!-- 상품 상세 카드 -->
    <v-container fluid class="product-detail-container py-12">
      <v-row justify="center">
        <v-col cols="12" sm="10" md="8" lg="6">
          <v-card class="product-card" elevation="2">
            <!-- 카드 헤더 -->
            <v-card-title class="title-gradient text-h5 font-weight-bold">
              {{ product?.fin_prdt_nm }}
            </v-card-title>
            <v-card-subtitle class="text-body-1 text-secondary">
              {{ product?.kor_co_nm }}
            </v-card-subtitle>

            <!-- 상품 정보 -->
            <v-card-text class="product-info-section py-4">
              <v-list>
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="primary" class="mr-3">mdi-account-check</v-icon>
                  </template>
                  <v-list-item-title>가입 조건</v-list-item-title>
                  <v-list-item-subtitle>{{ product?.join_member }}</v-list-item-subtitle>
                </v-list-item>

                <v-divider class="mx-4"></v-divider>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="primary" class="mr-3">mdi-hand-extended</v-icon>
                  </template>
                  <v-list-item-title>가입 방법</v-list-item-title>
                  <v-list-item-subtitle>{{ product?.join_way }}</v-list-item-subtitle>
                </v-list-item>

                <v-divider class="mx-4"></v-divider>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="primary" class="mr-3">mdi-star-circle</v-icon>
                  </template>
                  <v-list-item-title>특별 조건</v-list-item-title>
                  <v-list-item-subtitle>{{ product?.spcl_cnd || "없음" }}</v-list-item-subtitle>
                </v-list-item>

                <v-divider class="mx-4"></v-divider>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="primary" class="mr-3">mdi-information-outline</v-icon>
                  </template>
                  <v-list-item-title>기타 사항</v-list-item-title>
                  <v-list-item-subtitle>{{ product?.etc_note }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card-text>

            <!-- 액션 버튼 -->
            <v-card-actions class="justify-center pa-6">
              <v-btn
                block
                color="primary"
                variant="elevated"
                :loading="cartStore.isLoading"
                :disabled="cartStore.isProductInCart(product?.id) || !communityStore.isLogin"
                @click="addToCart"
                class="rounded-lg detail-btn"
              >
                <v-icon left class="mr-2 btn-icon">
                  {{ cartStore.isProductInCart(product?.id) ? 'mdi-check' : 'mdi-cart-plus' }}
                </v-icon>
                {{ getButtonText }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- 알림 메시지 -->
    <v-snackbar
      v-model="showSnackbar"
      :color="snackbarColor"
      timeout="3000"
      location="top"
    >
      {{ snackbarText }}
      <template v-slot:actions>
        <v-btn
          v-if="!communityStore.isLogin"
          color="white"
          text
          @click="goToLogin"
        >
          로그인
        </v-btn>
        <v-btn
          color="white"
          text
          @click="showSnackbar = false"
        >
          닫기
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router";
import { onMounted, ref, computed } from "vue";
import { useFinanceStore } from "@/stores/finance";
import { useCartStore } from "@/stores/cart";
import { useCommunityStore } from "@/stores/community";

const route = useRoute();
const router = useRouter();
const financeStore = useFinanceStore();
const cartStore = useCartStore();
const communityStore = useCommunityStore();
const product = ref(null);

// UI 상태 관리
const showSnackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');

// 버튼 텍스트 계산
const getButtonText = computed(() => {
  if (!communityStore.isLogin) {
    return '로그인 필요';
  }
  if (cartStore.isProductInCart(product.value?.id)) {
    return '장바구니에 있는 상품';
  }
  return '장바구니 담기';
});

// 장바구니 담기 함수
const addToCart = async () => {
  if (!product.value) return;
  
  try {
    await cartStore.addToCart({
      id: product.value.id,
      name: product.value.fin_prdt_nm,
      company: product.value.kor_co_nm,
      category: localStorage.getItem("selectedCategory"),
      options: product.value.options
    });

    snackbarText.value = '장바구니에 상품이 추가되었습니다';
    snackbarColor.value = 'success';
    showSnackbar.value = true;
  } catch (error) {
    snackbarText.value = error.message;
    snackbarColor.value = 'error';
    showSnackbar.value = true;
  }
};

// 로그인 페이지로 이동
const goToLogin = () => {
  router.push({ name: 'login' });
};

onMounted(async () => {
  const id = route.params.id;
  const selectedCategory = localStorage.getItem("selectedCategory");

  try {
    if (selectedCategory === "saving") {
      const savingsOptions = await financeStore.getSavingOptions(id);
      product.value = financeStore.savings.find((item) => item.id === Number(id));
      if (product.value) {
        product.value.options = savingsOptions;
      }
    } else if (selectedCategory === "deposit") {
      const depositOptions = await financeStore.getDepositOptions(id);
      product.value = financeStore.deposits.find((item) => item.id === Number(id));
      if (product.value) {
        product.value.options = depositOptions;
      }
    }
  } catch (error) {
    console.error("Error fetching product data:", error);
    snackbarText.value = '상품 정보를 불러오는데 실패했습니다';
    snackbarColor.value = 'error';
    showSnackbar.value = true;
  }

  // 사용자별 장바구니 로드
  cartStore.loadFromLocalStorage();
});
</script>

<style scoped>
.product-detail-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f7ff 0%, #e7f0f7 100%);
}

.product-card {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(8, 145, 178, 0.2);
  border-radius: 16px;
}

.title-gradient {
  background: linear-gradient(45deg, #0891b2, #0e7490);
  -webkit-background-clip: text;
  color: transparent;
}

.product-info-section {
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid rgba(8, 145, 178, 0.1);
}

.detail-btn {
  transition: all 0.3s ease-in-out;
}

.detail-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(8, 145, 178, 0.2);
}
</style>
