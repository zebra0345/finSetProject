<template>
  <div class="profile-container">
    <div class="content-wrapper">
      <!-- 왼쪽 섹션 - 차트 섹션 -->
      <div class="left-section">
        <div v-if="profileData?.nickName" class="chart-container">
          <h2 class="chart-title">금리 비교 차트</h2>
          
          <!-- 적금 상품 차트 -->
          <div v-if="savingItems.length > 0" class="chart-section">
            <h3 class="chart-subtitle">적금 상품 금리 비교</h3>
            <div class="chart">
              <Bar
                :data="getSavingChartData"
                :options="chartOptions"
              />
            </div>
          </div>

          <!-- 예금 상품 차트 -->
          <div v-if="depositItems.length > 0" class="chart-section">
            <h3 class="chart-subtitle">예금 상품 금리 비교</h3>
            <div class="chart">
              <Bar
                :data="getDepositChartData"
                :options="chartOptions"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 오른쪽 섹션 - 금리 비교표 -->
      <div class="right-section">
        <!-- 프로필 헤더 -->
        <div class="profile-header">
          <div v-if="profileData?.nickName" class="profile-header-content">
            <h1 class="profile-title">{{ profileData.nickName }}님의 금융상품 비교</h1>
          </div>

          <!-- 닉네임 설정 폼 -->
          <form v-else @submit.prevent="updateNickName" class="nickname-form">
            <h2 class="form-title">닉네임을 설정해주세요</h2>
            <div class="form-input">
              <label for="nickname" class="form-label">닉네임</label>
              <input 
                id="nickname"
                v-model="newNickName"
                type="text"
                placeholder="닉네임을 입력하세요"
                class="input-field"
              />
            </div>
            <button type="submit" class="submit-btn">저장</button>
          </form>
        </div>

        <!-- 금리 비교표 -->
        <div v-if="profileData?.nickName" class="comparison-section">
          <!-- 적금 상품 비교 -->
          <div v-if="savingItems.length > 0" class="table-section">
            <h2 class="table-title">적금 상품 비교</h2>
            <table class="rate-table">
              <thead>
                <tr>
                  <th>상품명</th>
                  <th>회사</th>
                  <th>금리</th>
                  <th>금리유형</th>
                  <th>액션</th>
                </tr>
              </thead>
              <tbody>
  <tr v-for="item in savingItems" :key="item.id">
    <td>{{ item.name }}</td>
    <td>{{ item.company }}</td>
    <td class="rate-cell">
      <span v-if="Array.isArray(item.options) && item.options.length > 0">
        {{ item.options[0].intr_rate }}%
      </span>
      <span v-else>
        {{ item.options.intr_rate }}%
      </span>
    </td>
    <td>
      <span v-if="Array.isArray(item.options) && item.options.length > 0">
        {{ item.options[0].intr_rate_type_nm }}
      </span>
      <span v-else>
        {{ item.options.intr_rate_type_nm }}
      </span>
    </td>
    <td>
      <button @click="removeFromCart(item.id)" class="remove-btn">
        삭제
      </button>
    </td>
  </tr>
</tbody>

            </table>
          </div>

          <!-- 예금 상품 비교 -->
          <div v-if="depositItems.length > 0" class="table-section">
            <h2 class="table-title">예금 상품 비교</h2>
            <table class="rate-table">
              <thead>
                <tr>
                  <th>상품명</th>
                  <th>회사</th>
                  <th>금리</th>
                  <th>금리유형</th>
                  <th>액션</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in depositItems" :key="item.id">
                  <td>{{ item.name }}</td>
                  <td>{{ item.company }}</td>
                  <td class="rate-cell">{{ item.options[0].intr_rate }}%</td>
                  <td>{{ item.options[0].intr_rate_type_nm }}</td>
                  <td>
                    <button @click="removeFromCart(item.id)" class="remove-btn">
                      삭제
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useCommunityStore } from '@/stores/community';
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';


ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default {
  components: {
    Bar
  },
  setup() {
    const store = useCommunityStore();
    const route = useRoute();
    const activeTab = ref('financial');
    const profileData = ref(null);
    const newNickName = ref('');
    const userId = store.user?.pk;
    const cart = ref(JSON.parse(localStorage.getItem(`cart_${userId}`) || '[]'));
    const savingItems = ref([]);
    const depositItems = ref([]);

    // 차트 옵션
    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        },
        title: {
          display: true,
          text: '금리 비교'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: '금리 (%)'
          },
          ticks: {
            callback: function(value) {
              return value + '%';
            }
          }
        },
        x: {
          title: {
            display: true,
            text: '상품명'
          }
        }
      }
    };

    // 적금 상품 차트 데이터
const getSavingChartData = computed(() => ({
  labels: savingItems.value.map(item => item.name),
  datasets: [{
    label: '적금 금리',
    data: savingItems.value.map(item => {
      if (Array.isArray(item.options) && item.options.length > 0) {
        return item.options[0].intr_rate;
      } else {
        return item.options.intr_rate;
      }
    }),
    backgroundColor: 'rgba(8, 145, 178, 0.6)',
    borderColor: 'rgba(8, 145, 178, 1)',
    borderWidth: 1
  }]
}));


    // 예금 상품 차트 데이터
    const getDepositChartData = computed(() => ({
      labels: depositItems.value.map(item => item.name),
      datasets: [{
        label: '예금 금리',
        data: depositItems.value.map(item => item.options[0].intr_rate),
        backgroundColor: 'rgba(14, 116, 144, 0.6)',
        borderColor: 'rgba(14, 116, 144, 1)',
        borderWidth: 1
      }]
    }));

    // 카트에서 상품 제거
    const removeFromCart = (itemId) => {
      cart.value = cart.value.filter(item => item.id !== itemId);
      localStorage.setItem(`cart_${userId}`, JSON.stringify(cart.value));
      filterCartItems();
    };

    const fetchProfileData = async () => {
      try {
        const userId = route.params.id;
        const data = await store.fetchUserById(userId);
        profileData.value = data;
      } catch (error) {
        console.error('프로필 정보를 불러오는데 실패했습니다:', error);
      }
    };

    const filterCartItems = () => {
      savingItems.value = cart.value.filter(item => item.category === 'saving');
      depositItems.value = cart.value.filter(item => item.category === 'deposit');
    };

    const updateNickName = async () => {
  if (!newNickName.value.trim()) {
    alert("닉네임을 입력해주세요.");
    return;
  }

  const userId = route.params.id; // URL에서 user ID 가져오기
  
  try {
    // POST 요청
    const userToken = ref(localStorage.getItem('community'))
    const response = await axios.post(
      `http://127.0.0.1:8000/accounts/profile/${userId}/`,
      { nickName: newNickName.value }, // 전송 데이터
      {
        headers: {
          Authorization: `Token ${JSON.parse(userToken.value).token}`, // 인증 토큰 (필요 시)
        },
      }
    );

    // 성공적으로 닉네임이 저장된 경우
    profileData.value.nickName = response.data.nickName; // 반환된 데이터로 업데이트
    newNickName.value = ""; // 입력값 초기화
    alert("닉네임이 성공적으로 저장되었습니다.");
  } catch (err) {
    console.error("닉네임 업데이트 중 오류 발생:", err);
    alert("닉네임 저장에 실패했습니다. 다시 시도해주세요.");
  }
};

    const fetchNickName = () => {
      if (!userId) return;
      const storageKey = `userNickName_${userId}`;
      const storedNickName = localStorage.getItem(storageKey);
      if (storedNickName) {
        profileData.value = { ...profileData.value, nickName: storedNickName };
      }
    };

    onMounted(() => {
      fetchProfileData();
      filterCartItems();
      fetchNickName();
    });

    return {
      activeTab,
      profileData,
      newNickName,
      savingItems,
      depositItems,
      updateNickName,
      removeFromCart,
      chartOptions,
      getSavingChartData,
      getDepositChartData
    };
  }
};
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f7ff 0%, #e6f0f9 100%);
  padding: 20px;
}

.content-wrapper {
  display: flex;
  gap: 30px;
  max-width: 1400px;
  margin: 0 auto;
  flex-direction: row;
}

.left-section {
  flex: 1;
  min-width: 0;
}

.right-section {
  width: 600px;
  flex-shrink: 0;
}

.chart-container {
  background-color: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(8, 145, 178, 0.1);
  margin-bottom: 20px;
}

.chart-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 20px;
}

.chart-section {
  margin-bottom: 30px;
}

.chart-subtitle {
  font-size: 1.2rem;
  color: #1e293b;
  margin-bottom: 15px;
}

.chart {
  height: 300px;
  margin-bottom: 20px;
}

.table-section {
  background-color: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(8, 145, 178, 0.1);
  margin-bottom: 20px;
}

.table-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 15px;
}

.rate-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #f9fafb;
  border-radius: 8px;
  overflow: hidden;
}

.rate-table th,
.rate-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.rate-table th {
  background-color: #f3f4f6;
  font-weight: 600;
  color: #1e293b;
}

.rate-cell {
  font-weight: 600;
  color: #0891b2;
}

.remove-btn {
  padding: 4px 8px;
  background-color: #ef4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.remove-btn:hover {
  background-color: #dc2626;
}

.profile-header {
  background-color: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(8, 145, 178, 0.1);
  margin-bottom: 20px;
}

.profile-header-content {
  margin-bottom: 20px;
}

.profile-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
}

.nickname-form {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
}

.form-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: #1e293b;
}

.form-input {
  margin-bottom: 20px;
}

.form-label {
  font-size: 1rem;
  color: #4b5563;
}

.input-field {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  margin-top: 4px;
}

.submit-btn {
  background-color: #0891b2;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  width: 100%;
  font-weight: 600;
  cursor: pointer;
  border: none;
}

.submit-btn:hover {
  background-color: #0e7490;
}

@media (max-width: 1200px) {
  .content-wrapper {
    flex-direction: column;
  }

  .left-section,
  .right-section {
    width: 100%;
  }

  .chart-container {
    margin-bottom: 30px;
  }
}

/* 기존 스타일 유지 */
.profile-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f7ff 0%, #e6f0f9 100%);
  padding: 20px;
}
.content-wrapper {
  display: flex;
  gap: 30px;
  max-width: 1400px;
  margin: 0 auto;
}

.left-section {
  flex: 1;
  min-width: 0; /* flex item 축소 허용 */
}

.right-section {
  width: 400px;
  flex-shrink: 0; /* 크기 고정 */
}

.comparison-table {
  background-color: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(8, 145, 178, 0.1);
  position: sticky;
  top: 20px;
}

.comparison-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 20px;
}

.table-section {
  margin-bottom: 30px;
}

.table-subtitle {
  font-size: 1.2rem;
  color: #1e293b;
  margin-bottom: 15px;
}

.rate-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #f9fafb;
  border-radius: 8px;
  overflow: hidden;
}

.rate-table th,
.rate-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.rate-table th {
  background-color: #f3f4f6;
  font-weight: 600;
  color: #1e293b;
}

.rate-table tr:last-child td {
  border-bottom: none;
}

.rate-cell {
  font-weight: 600;
  color: #0891b2;
}

/* 반응형 디자인 */
@media (max-width: 1024px) {
  .content-wrapper {
    flex-direction: column;
  }

  .right-section {
    width: 100%;
  }

  .comparison-table {
    position: static;
  }
}


.profile-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f7ff 0%, #e6f0f9 100%);
  padding: 20px;
}

.profile-header {
  background-color: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(8, 145, 178, 0.1);
}

.profile-header-content {
  margin-bottom: 20px;
}

.profile-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
}

.nickname-form {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(8, 145, 178, 0.1);
}

.form-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: #1e293b;
}

.form-input {
  margin-bottom: 20px;
}

.form-label {
  font-size: 1rem;
  color: #4b5563;
}

.input-field {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
}

.submit-btn {
  background-color: #0891b2;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  width: 100%;
  font-weight: 600;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #0e7490;
}

.cart-info {
  margin-top: 40px;
}

.financial-products {
  padding: 20px;
}

.product-list {
  margin-top: 20px;
}

.product-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.product-card {
  background-color: #f9fafb;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(8, 145, 178, 0.1);
  transition: all 0.3s ease;
}

.product-card:hover {
  box-shadow: 0 4px 15px rgba(8, 145, 178, 0.2);
}

.product-card-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.product-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
}

.product-details {
  font-size: 1rem;
  color: #4b5563;
  margin-bottom: 5px;
}
</style>
