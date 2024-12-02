<template>
  <v-container class="calculator-container">
    <!-- 제목 섹션 -->
    <v-row justify="center">
      <v-col cols="12" class="text-center mb-8">
        <h1 class="text-h3 font-weight-bold gradient-text">
          환율 계산기
        </h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          손쉽게 환율을 계산하세요!
        </p>
      </v-col>
    </v-row>

    <!-- 날짜 선택 -->
    <v-row class="mb-6">
      <v-col cols="12" sm="6">
        <v-text-field
          v-model="searchDate"
          label="검색 날짜"
          type="date"
          outlined
          prepend-icon="mdi-calendar"
          class="theme-input"
          @change="getExchangeRates"
        ></v-text-field>
      </v-col>
    </v-row>

    <!-- 통화 선택 -->
    <v-row v-if="exchangeRates.length > 0" class="mb-6">
      <v-col cols="12" sm="6">
        <v-select
          v-model="fromCurrency"
          :items="currencyList"
          label="출발 통화"
          outlined
          class="theme-select"
          prepend-icon="mdi-currency-usd"
        ></v-select>
      </v-col>

      <v-col cols="12" sm="6">
        <v-select
          v-model="toCurrency"
          :items="currencyList"
          label="도착 통화"
          outlined
          class="theme-select"
          prepend-icon="mdi-currency-usd"
        ></v-select>
      </v-col>
    </v-row>

    <!-- 금액 입력 및 계산 -->
    <v-row v-if="fromCurrency && toCurrency" class="mb-6">
      <v-col cols="12" sm="6">
        <v-text-field
          v-model="amount"
          label="금액 입력"
          type="number"
          outlined
          class="theme-input"
          prepend-icon="mdi-cash"
          placeholder="금액을 입력하세요"
          @input="clearResult"
        ></v-text-field>
      </v-col>

      <v-col cols="12" sm="6">
        <v-btn
          @click="calculateExchange"
          class="calculate-btn"
          color="primary"
          block
        >
          계산하기
          <v-icon right>mdi-arrow-right-bold</v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <!-- 계산 결과 -->
    <v-row v-if="calculatedAmount !== null">
      <v-col cols="12" class="text-center">
        <v-card class="result-card" elevation="2">
          <v-card-text>
            <p class="result-text">
              <strong>{{ amount }}</strong> {{ fromCurrency }} = 
              <span class="highlight">{{ calculatedAmount.toFixed(2) }}</span> {{ toCurrency }}
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 에러 메시지 -->
    <v-row v-if="error">
      <v-col cols="12" class="text-center">
        <v-alert type="error" dense class="theme-alert">
          {{ error }}
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchDate: '',
      exchangeRates: [],
      currencyList: [],
      fromCurrency: '',
      toCurrency: '',
      amount: null,
      calculatedAmount: null,
      error: null,
    };
  },
  methods: {
    async getExchangeRates() {
      if (!this.searchDate) {
        this.error = "날짜를 선택해주세요.";
        return;
      }
      this.error = null;
      try {
        const response = await axios.get('http://127.0.0.1:8000/exchanges/', {
          params: { searchdate: this.searchDate },
        });
        this.exchangeRates = response.data.result;
        this.currencyList = Array.from(
          new Set(this.exchangeRates.map(rate => rate.cur_unit))
        );
      } catch (err) {
        this.error = '환율 정보를 가져오는 데 실패했습니다.';
        console.error(err);
      }
    },

    calculateExchange() {
      if (!this.amount || this.amount <= 0) {
        this.error = "금액을 입력해주세요.";
        return;
      }
      this.error = null;

      const fromRate = this.exchangeRates.find(rate => rate.cur_unit === this.fromCurrency);
      const toRate = this.exchangeRates.find(rate => rate.cur_unit === this.toCurrency);

      if (!fromRate || !toRate) {
        this.error = "선택한 통화에 대한 환율 정보를 찾을 수 없습니다.";
        return;
      }

      const fromRateValue = parseFloat(fromRate.deal_bas_r);
      const toRateValue = parseFloat(toRate.deal_bas_r);

      if (isNaN(fromRateValue) || isNaN(toRateValue)) {
        this.error = "환율 정보가 유효하지 않습니다.";
        return;
      }

      if (this.fromCurrency === 'KRW') {
        this.calculatedAmount = this.amount * toRateValue;
      } else if (this.toCurrency === 'KRW') {
        this.calculatedAmount = this.amount / fromRateValue;
      } else {
        this.calculatedAmount = (this.amount / fromRateValue) * toRateValue;
      }
    },

    clearResult() {
      this.calculatedAmount = null;
    },
  },
};
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.calculator-container {
  padding: 24px;
  background: linear-gradient(135deg, #e3f2fd, #e7f0f7);
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* 제목 스타일 */
.gradient-text {
  background: linear-gradient(45deg, #007BFF, #1E88E5);
  -webkit-background-clip: text;
  color: transparent;
}

/* 입력 및 버튼 스타일 */
.theme-input {
  background-color: #ffffff;
  border-radius: 8px;
  color: #1E293B;
}

.theme-select {
  background-color: #ffffff;
  border-radius: 8px;
  color: #1E293B;
}

.calculate-btn {
  font-size: 1.1rem;
  border-radius: 8px;
}

/* 결과 카드 */
.result-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 16px;
}

.result-text {
  font-size: 1.5rem;
  color: #1E88E5;
}

.highlight {
  color: #FF5722;
  font-weight: bold;
}
</style>
