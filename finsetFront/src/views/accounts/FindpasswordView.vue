<template>
  <div class="find-password-container">
    <h1 class="title">비밀번호 찾기</h1>
    <form @submit.prevent="handleFindPassword">
      <div class="form-group">
        <label for="email">이메일</label>
        <input
          v-model="email"
          type="email"
          id="email"
          placeholder="가입한 이메일 주소를 입력하세요"
          required
        />
      </div>
      <button type="submit" class="find-password-button">비밀번호 찾기</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
    };
  },
  methods: {
    handleFindPassword() {
      console.log("비밀번호 찾기 요청:", this.email);
    },
  },
};
</script>

<style scoped>
.find-password-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 40px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #ffffff;
}

.title {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.find-password-button {
  width: 100%;
  padding: 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.find-password-button:hover {
  background-color: #0056b3;
}
</style>
