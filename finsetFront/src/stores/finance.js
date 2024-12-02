import { ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useFinanceStore = defineStore("finance", () => {
  const API_URL = "http://127.0.0.1:8000";

  // 금융 데이터를 저장하는 반응형 배열
  const savings = ref([]);
  const deposits = ref([]);
  const options = ref([]); // 옵션 데이터
  const selectedCategory = ref(localStorage.getItem("selectedCategory") || ""); // 로컬스토리지에서 가져오기

  // 금융 데이터를 조회하는 메서드 - 적금
  const getSavings = function () {
    axios({
      method: "get",
      url: `${API_URL}/finSetApp/SavingProductsAll/`,
    })
      .then((res) => {
        savings.value = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
  };

  // 금융 데이터를 조회하는 메서드 - 예금
  const getDeposits = function () {
    axios({
      method: "get",
      url: `${API_URL}/finSetApp/depositProductsAll/`,
    })
      .then((res) => {
        deposits.value = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
  };

  // 예금 옵션 조회
  const getDepositOptions = async function (productId) {
    try {
      const res = await axios.get(`${API_URL}/finSetApp/depositOptions/${productId}/`);
      console.log(`Deposit options for ${productId}:`, res.data); // 디버깅용 로그
      return res.data; // 예금 옵션 반환
    } catch (error) {
      console.error("Error fetching deposit options:", error);
      return []; // 오류 시 빈 배열 반환
    }
  };

  // 적금 옵션 조회
  const getSavingOptions = async function (productId) {
    try {
      const res = await axios.get(`${API_URL}/finSetApp/SavingOptions/${productId}/`);
      console.log(`Saving options for ${productId}:`, res.data); // 디버깅용 로그
      return res.data; // 적금 옵션 반환
    } catch (error) {
      console.error("Error fetching saving options:", error);
      return []; // 오류 시 빈 배열 반환
    }
  };

  // 선택된 카테고리에 따라 옵션을 가져오는 메서드
  const getProductOptions = async function (productId) {
    if (!productId) {
      console.error("상품 ID가 제공되지 않았습니다.");
      return;
    }

    // 로컬스토리지에서 카테고리 확인
    const category = selectedCategory.value;

    if (category === "deposit") {
      // 예금인 경우
      options.value = await getDepositOptions(productId);
    } else if (category === "savings") {
      // 적금인 경우
      options.value = await getSavingOptions(productId);
    } else {
      console.error("잘못된 카테고리 값입니다:", category);
    }
  };

  return {
    API_URL,
    savings,
    getSavings,
    deposits,
    getDeposits,
    getDepositOptions,
    getSavingOptions,
    getProductOptions, // 선택된 상품의 옵션을 가져오는 메서드
    options,
    selectedCategory, // 현재 선택된 카테고리
  };
},{ persist: true });
