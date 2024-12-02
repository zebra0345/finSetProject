import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { defineStore } from "pinia";
import apiClient from "@/utils/api";
import axios from "axios";

export const useCommunityStore = defineStore("community", () => {
  const token = ref({});
  const isLogin = computed(() => !!token.value);
  const router = useRouter();
  const user = ref(null);
  
  // 기존 로그인 함수
  const logIn = async (payload) => {
    const { username, password } = payload;
    try {
      const res = await apiClient.post("http://127.0.0.1:8000/accounts/auth/login/", { 
        username, 
        password 
      });
      token.value = res.data.key;
      console.log(token.value, res.data, "??????")
      alert("로그인 성공!");
      router.push({ name: "home" });
    } catch (err) {
      console.error(err.response?.data || err);
      alert("로그인 실패: 아이디나 비밀번호를 확인하세요.");
    }
  };

  // 기존 로그아웃 함수
  const logOut = async () => {
    try {
      const response = await apiClient.post("http://127.0.0.1:8000/accounts/auth/logout/", {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });

      if (response.status === 200) {
        token.value = null
        localStorage.removeItem("accessToken");
        alert("로그아웃되었습니다.");
        router.push({ name: "home" });
      }
    } catch (err) {
      console.error("로그아웃 실패:", err);
      alert("로그아웃 중 문제가 발생했습니다.");
    }
  };

  // 기존 유저 정보 조회 함수
  const fetchUserInfo = async () => {
    try {
      if (!token.value) return;
      const response = await apiClient.get("http://127.0.0.1:8000/accounts/auth/user/", {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      user.value = response.data;
      console.log("유저 정보:", user.value);
    } catch (err) {
      console.error("유저 정보 요청 실패:", err);
      user.value = null;
    }
  };

  // 기존 회원가입 함수
  const signUp = async (payload) => {
    const { username, email, password1, password2 } = payload;
    try {
      await apiClient.post("/accounts/registration/", {
        username,
        email,
        password1,
        password2,
      });
      alert("회원가입 성공! 로그인 페이지로 이동합니다.");
      router.push({ name: "login" });
    } catch (err) {
      console.error("회원가입 실패:", err.response?.data || err);
      alert("회원가입 중 문제가 발생했습니다. 입력 정보를 다시 확인해주세요.");
    }
  };

  // 프로필 정보 조회 (백엔드 URL에 맞게 수정)
  const fetchUserById = async (userId) => {
    try {
      const response = await apiClient.get(`http://127.0.0.1:8000/accounts/profile/${userId}/`, {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      return response.data;
    } catch (err) {
      console.error("프로필 정보 조회 실패:", err);
      throw err;
    }
  };

  // 예금 추가
  const addDeposit = async (profileId, depositId) => {
    try {
      const response = await apiClient.post(`http://127.0.0.1:8000/accounts/deposit/${profileId}/${depositId}/`, {}, {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      alert("예금이 성공적으로 추가되었습니다.");
      return response.data;
    } catch (err) {
      console.error("예금 추가 실패:", err);
      alert("예금 추가 중 문제가 발생했습니다.");
      throw err;
    }
  };

  // 적금 추가
  const addSaving = async (profileId, savingId) => {
    try {
      const response = await apiClient.post(`http://127.0.0.1:8000/accounts/saving/${profileId}/${savingId}/`, {}, {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      alert("적금이 성공적으로 추가되었습니다.");
      return response.data;
    } catch (err) {
      console.error("적금 추가 실패:", err);
      alert("적금 추가 중 문제가 발생했습니다.");
      throw err;
    }
  };

  // 프로필 업데이트 (백엔드에서 지원하는 경우)
  const updateUserProfile = async (userId, userData) => {
    try {
      const response = await apiClient.post(`http://127.0.0.1:8000/accounts/profile/${userId}/`, userData, {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      alert("프로필이 성공적으로 업데이트되었습니다.");
      return response.data;
    } catch (err) {
      console.error("프로필 업데이트 실패:", err);
      alert("프로필 업데이트 중 문제가 발생했습니다.");
      throw err;
    }
  };

  return {
    isLogin,
    logIn,
    logOut,
    signUp,
    token,
    user,
    fetchUserInfo,
    fetchUserById,
    updateUserProfile,
    addDeposit,
    addSaving,
  };
}, { persist: true });