<template>
  <header class="header">
    <nav class="nav-bar">
      <RouterLink :to="{name:'home'}" class="logo">
        <img src="/logo.jpeg" alt="Finset Logo" style="width: 150px;" />
      </RouterLink>
      <ul class="nav-links">
        <li v-if="store.user?.pk && store.isLogin">
          <RouterLink 
            @click.prevent="FindId" 
            :to="{name:'profile', params:{'id':store.user?.pk || 0}}" 
            class="nav-link"
          >
            {{ user || "Guest" }}
          </RouterLink>
        </li>


        <li v-if="store.isLogin">
          <v-btn
          to="/modify"
          class="financial-btn mx-1"
          text
        >
          <v-icon left>mdi-cog</v-icon>
          내 정보
        </v-btn>
        </li>
        <li v-if="store.isLogin">
          <v-btn
          to="/boards"
          class="financial-btn mx-1"
          text
        >
          <v-icon left>mdi-forum</v-icon>
          게시판
        </v-btn>
        </li>
        <li v-if="!store.isLogin">
          <v-btn
          to="/login"
          class="financial-btn mx-1"
          text
        >
          <v-icon left>mdi-login</v-icon>
          로그인
        </v-btn>
        </li>
        <li v-if="!store.isLogin">
          <v-btn
          to="/signup"
          class="signup-btn mx-1"
          color="primary"
          elevation="2"
        >
          <v-icon left>mdi-account-plus</v-icon>
          회원가입
        </v-btn>
        </li>
        <li v-else>
          <v-btn
          @click="handleLogout"
          class="logout-btn mx-1"
          outlined
          color="error"
        >
          <v-icon left>mdi-logout</v-icon>
          로그아웃
        </v-btn>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
import { useCommunityStore } from "@/stores/community";
import { onMounted } from "vue";

export default {
  setup() {
  const store = useCommunityStore();

  const FindId = () => {
  if (store.user?.pk) {
    store.fetchUserInfo();
  } else {
    console.log("User 정보가 없습니다.");
  }
};


  const handleLogout = () => {
    store.logOut();
  };

  const user = store.user?.username || "Guest";



  // 컴포넌트가 마운트될 때 사용자 정보 가져오기
  onMounted(() => {
  if (store.isLogin && !store.user?.pk) {
    store.fetchUserInfo();
  }
});


  return {
    FindId,
    store,
    handleLogout,
    user
  };
},

};
</script>

<style scoped>
/* 헤더 스타일 */
.header {
  background-color: #e7f0f7;
  padding: 10px 20px;
  border-bottom: 1px solid #ccc;
}

/* 네비게이션 바 스타일 */
.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 네비게이션 링크 스타일 */
.nav-links {
  list-style: none;
  display: flex;
  gap: 15px;
  align-items: center;
  margin: 0;
  padding: 0;
}

.nav-links li {
  display: inline-block;
}

/* 일반 링크 스타일 */
.nav-link {
  color: #2c3e50;
  text-decoration: none;
  font-weight: 600;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  background: linear-gradient(90deg, #e3f2fd, #ffffff);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.nav-link:hover {
  color: #ffffff;
  background: linear-gradient(90deg, #1a73e8, #42a5f5);
  box-shadow: 0 6px 12px rgba(26, 115, 232, 0.2);
}

/* 회원가입 버튼 */
.nav-button {
  background: linear-gradient(90deg, #1a73e8, #42a5f5);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.nav-button:hover {
  background: linear-gradient(90deg, #1557b0, #1a73e8);
  box-shadow: 0 6px 12px rgba(26, 115, 232, 0.3);
  transform: scale(1.05);
}

/* 로그아웃 버튼 */
.logout-button {
  background: transparent;
  color: #dc3545;
  border: 1px solid #dc3545;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.logout-button:hover {
  background-color: #dc3545;
  color: white;
  box-shadow: 0 6px 12px rgba(220, 53, 69, 0.3);
  transform: scale(1.05);
}
</style>
