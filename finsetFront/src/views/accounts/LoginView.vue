<template>
  <div class="login-container">
    <h1 class="title">로그인</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">아이디</label>
        <input
          id="username"
          type="text"
          placeholder="아이디를 입력하세요"
          @input="updateUsername"
        />
      </div>
      <div class="form-group">
        <label for="password">비밀번호</label>
        <input
          id="password"
          type="password"
          placeholder="비밀번호를 입력하세요"
          @input="updatePassword"
        />
      </div>
      <button type="submit" class="login-button">로그인</button>
    </form>

    <div class="links">
      <RouterLink to="/signup" class="link">회원가입</RouterLink>
      <RouterLink to="/findpassword" class="link">비밀번호 찾기</RouterLink>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useCommunityStore } from "@/stores/community";

export default {
  setup() {
    const store = useCommunityStore();
    const username = ref("");
    const password = ref("");

    const updateUsername = (event) => {
      username.value = event.target.value;
    };

    const updatePassword = (event) => {
      password.value = event.target.value;
    };

    const handleLogin = () => {
      if (!username.value || !password.value) {
        alert("아이디와 비밀번호를 입력해주세요.");
        return;
      }
      store.logIn({ username: username.value, password: password.value });
    };

    return {
      updateUsername,
      updatePassword,
      handleLogin,
    };
  },
};
</script>

<style scoped>
/* 로그인 컨테이너 스타일 */
.login-container {
  max-width: 400px;
  min-height: 500px;
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

/* 로그인 버튼 스타일 */
.login-button {
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

.login-button:hover {
  background: linear-gradient(90deg, #1557b0, #1a73e8);
  box-shadow: 0 6px 12px rgba(26, 115, 232, 0.3);
  transform: scale(1.02);
}

/* 링크 스타일 */
.links {
  margin-top: 20px;
}

.link {
  font-size: 1rem;
  color: #1a73e8;
  text-decoration: none;
  margin: 0 10px;
  transition: all 0.3s ease;
}

.link:hover {
  color: #0a4c5c;
  text-decoration: underline;
}
</style>
