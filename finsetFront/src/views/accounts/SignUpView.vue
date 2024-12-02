<template>
  <div class="signup-container">
    <h1 class="title">회원가입</h1>
    <form @submit.prevent="handleSignUp">
      <div class="form-group">
        <label for="username">아이디</label>
        <input
          v-model="username"
          type="text"
          id="username"
          placeholder="아이디를 입력하세요"
          required
        />
      </div>
      <div class="form-group">
        <label for="email">이메일</label>
        <input
          v-model="email"
          type="email"
          id="email"
          placeholder="이메일을 입력하세요"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">비밀번호</label>
        <input
          v-model="password"
          type="password"
          id="password"
          placeholder="비밀번호를 입력하세요"
          required
        />
      </div>
      <div class="form-group">
        <label for="confirm-password">비밀번호 확인</label>
        <input
          v-model="confirmPassword"
          type="password"
          id="confirm-password"
          placeholder="비밀번호를 다시 입력하세요"
          required
        />
      </div>
      <button type="submit" class="signup-button">회원가입</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
    };
  },
  methods: {
    async handleSignUp() {
      if (this.password !== this.confirmPassword) {
        alert("비밀번호가 일치하지 않습니다.");
        return;
      }

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/accounts/registration/",
          {
            username: this.username,
            email: this.email,
            password1: this.password,
            password2: this.confirmPassword,
          }
        );
        console.log("회원가입 성공:", response.data);

        alert("회원가입이 완료되었습니다. 로그인 페이지로 이동합니다.");
        this.$router.push({ name: "login" }); // 로그인 페이지로 이동
      } catch (error) {
        console.error("회원가입 실패:", error.response.data);
        alert("회원가입에 실패했습니다. 입력 정보를 확인하세요.");
      }
    },
  },
};
</script>

<style scoped>
/* 회원가입 컨테이너 스타일 */
.signup-container {
  max-width: 450px;
  min-height: 650px;
  margin: 50px auto;
  padding: 40px;
  border-radius: 12px;
  background: linear-gradient(145deg, #f0f7ff, #ffffff);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* 제목 스타일 */
.title {
  font-size: 2rem;
  font-weight: bold;
  color: #0a4c5c;
  margin-bottom: 30px;
}

/* 폼 그룹 스타일 */
.form-group {
  margin-bottom: 20px;
  text-align: left;
}

.form-group label {
  font-size: 1rem;
  color: #0a4c5c;
  margin-bottom: 8px;
  display: block;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9fbfd;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus {
  border-color: #1a73e8;
  box-shadow: 0 0 5px rgba(26, 115, 232, 0.3);
  outline: none;
}

/* 회원가입 버튼 스타일 */
.signup-button {
  width: 100%;
  padding: 15px;
  background: linear-gradient(90deg, #1a73e8, #42a5f5);
  color: white;
  font-size: 1.2rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.signup-button:hover {
  background: linear-gradient(90deg, #1557b0, #1a73e8);
  box-shadow: 0 6px 12px rgba(26, 115, 232, 0.3);
  transform: scale(1.02);
}
</style>
