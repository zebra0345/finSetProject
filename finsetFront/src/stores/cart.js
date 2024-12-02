// stores/cart.js
import { defineStore } from 'pinia';
import { useCommunityStore } from '@/stores/community';
import apiClient from "@/utils/api";

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    loading: false,
    error: null,
  }),

  getters: {
    cartItems: (state) => state.items,
    cartItemCount: (state) => state.items.length,
    isLoading: (state) => state.loading,
    hasError: (state) => !!state.error,
  },

  actions: {
    async addToCart(product) {
      const communityStore = useCommunityStore();
      
      // 로그인 체크
      if (!communityStore.isLogin) {
        throw new Error('로그인이 필요한 서비스입니다.');
      }

      try {
        this.loading = true;
        this.error = null;

        // 이미 장바구니에 있는지 확인
        if (this.items.some(item => item.id === product.id)) {
          throw new Error('이미 장바구니에 있는 상품입니다');
        }

        const newCartItem = {
          ...product,
          addedAt: new Date().toISOString(),
          userId: communityStore.user?.pk || communityStore.user?.id,
        };

        // 장바구니에 추가
        this.items.push(newCartItem);
        this.saveToLocalStorage();

        // 상품 타입에 따라 서버에 추가 요청
        if (product.category === 'deposit') {
          await communityStore.addDeposit(communityStore.user.pk, product.id);
        } else if (product.category === 'saving') {
          await communityStore.addSaving(communityStore.user.pk, product.id);
        }

      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    removeFromCart(productId) {
      this.items = this.items.filter(item => item.id !== productId);
      this.saveToLocalStorage();
    },

    clearCart() {
      this.items = [];
      this.saveToLocalStorage();
    },

    isProductInCart(productId) {
      return this.items.some(item => item.id === productId);
    },

    // 로컬 스토리지에 장바구니 상태 저장
    saveToLocalStorage() {
      const communityStore = useCommunityStore();
      const userId = communityStore.user?.pk || communityStore.user?.id;
      
      if (userId) {
        const cartKey = `cart_${userId}`;
        localStorage.setItem(cartKey, JSON.stringify(this.items));
      }
    },

    // 로컬 스토리지에서 장바구니 상태 로드
    loadFromLocalStorage() {
      const communityStore = useCommunityStore();
      const userId = communityStore.user?.pk || communityStore.user?.id;
      
      if (userId) {
        const cartKey = `cart_${userId}`;
        const savedCart = localStorage.getItem(cartKey);
        if (savedCart) {
          this.items = JSON.parse(savedCart);
        }
      }
    },

    // 로그아웃 시 장바구니 초기화
    resetCart() {
      this.items = [];
      this.error = null;
      this.loading = false;
    },
  },
});