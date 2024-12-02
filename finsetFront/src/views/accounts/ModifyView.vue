<template>
  <v-container class="medical-settings">
    <v-card class="pa-4">
      <v-card-title class="text-h4 d-flex align-center mb-6">
        <v-icon large color="primary" class="mr-3">mdi-account</v-icon>
        회원 정보 관리
      </v-card-title>

      <!-- 회원 정보 수정 섹션 -->
      <v-card class="mb-6" elevation="2">
        <v-card-title class="subtitle-1">
          <v-icon color="primary" class="mr-2">mdi-account-edit</v-icon>
          회원 정보 수정
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="updateNickName">
            <v-text-field
              v-model="updatedNickName"
              label="닉네임"
              prepend-icon="mdi-account"
              :rules="[v => !!v || '닉네임을 입력해주세요']"
              placeholder="새로운 닉네임"
              outlined
              dense
              class="mb-4"
            ></v-text-field>
            <v-btn
              type="submit"
              color="primary"
              class="medical-btn"
              :loading="loading"
            >
              <v-icon left>mdi-content-save</v-icon>
              저장
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>

      <!-- 회원 탈퇴 섹션 -->
      <v-card class="error-card" elevation="2">
        <v-card-title class="subtitle-1">
          <v-icon color="error" class="mr-2">mdi-account-remove</v-icon>
          회원 탈퇴
        </v-card-title>
        <v-card-text>
          <v-alert
            type="warning"
            dense
            border="left"
            colored-border
            elevation="2"
            class="mb-4"
          >
            <div class="text-subtitle-2">주의사항</div>
            <ul class="mt-2">
              <li>탈퇴 시 모든 정보가 완전히 삭제됩니다.</li>
              <li>삭제된 정보는 복구가 불가능합니다.</li>
              <li>상품 가입 기록이 있다면 법정 보관 기간 동안 별도 저장됩니다.</li>
            </ul>
          </v-alert>
          <v-btn
            color="error"
            class="medical-btn"
            @click="showDeleteDialog = true"
          >
            <v-icon left>mdi-delete</v-icon>
            회원 탈퇴
          </v-btn>
        </v-card-text>
      </v-card>

      <!-- 회원 탈퇴 확인 다이얼로그 -->
      <v-dialog v-model="showDeleteDialog" max-width="400">
        <v-card>
          <v-card-title class="headline error--text">
            <v-icon color="error" class="mr-2">mdi-alert</v-icon>
            회원 탈퇴 확인
          </v-card-title>
          <v-card-text class="pt-4">
            정말로 회원 탈퇴를 진행하시겠습니까?
            <br>이 작업은 취소할 수 없습니다.
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="grey darken-1"
              text
              @click="showDeleteDialog = false"
            >
              취소
            </v-btn>
            <v-btn
              color="error"
              @click="deleteAccount"
              :loading="loading"
            >
              탈퇴하기
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card>
  </v-container>
</template>

<script>
import { useCommunityStore } from "@/stores/community";
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";

export default {
  setup() {
    const updatedNickName = ref("");
    const store = useCommunityStore();
    const loading = ref(false);
    const showDeleteDialog = ref(false);
    const router = useRouter()
    
    const updateNickName = async () => {
      if (!updatedNickName.value) return;
      
      loading.value = true;
      try {
        const userToken = ref(localStorage.getItem("community"));
        const userPk = store.user.pk;

        const response = await axios.post(
          `http://127.0.0.1:8000/accounts/profile/${userPk}/`,
          { nickName: updatedNickName.value },
          {
            headers: { Authorization: `Token ${JSON.parse(userToken.value).token}` },
          }
        );

        response.data.nickName = updatedNickName.value;
        store.fetchUserById(store.user.pk).nickName = response.data.nickName;
        updatedNickName.value = '';
        
        // Vuetify 스낵바로 변경하면 좋을 것 같습니다
        alert("닉네임이 성공적으로 수정되었습니다.");
        console.log(userPk)
        router.push({ name: "profile", params:{id:userPk}})
      } catch (error) {
        console.error("닉네임 수정 실패:", error);
        alert("닉네임 수정 중 오류가 발생했습니다.");
      } finally {
        loading.value = false;
      }
    };

    const deleteAccount = async () => {
      loading.value = true;
      try {
        const userToken = ref(localStorage.getItem("community"));
        await axios.delete("http://127.0.0.1:8000/accounts/delete_user/", {
          headers: { Authorization: `Token ${JSON.parse(userToken.value).token}` },
        });
        
        localStorage.removeItem("community");
        store.logOut();
        window.location.href = "/";
      } catch (error) {
        console.error("회원 탈퇴 실패:", error);
        alert("회원 탈퇴 중 오류가 발생했습니다.");
      } finally {
        loading.value = false;
        showDeleteDialog.value = false;
      }
    };

    return {
      updatedNickName,
      updateNickName,
      deleteAccount,
      loading,
      showDeleteDialog,
    };
  },
};
</script>

<style scoped>
.medical-settings {
  max-width: 800px;
  margin: 0 auto;
}

.medical-btn {
  text-transform: none !important;
  letter-spacing: 0 !important;
}

.error-card {
  border-left: 4px solid var(--v-error-base) !important;
}

/* Vuetify 테마 커스텀을 위한 변수 설정 예시 */
:root {
  --v-primary-base: #2196F3; /* 의료용 파랑 */
  --v-error-base: #FF5252;   /* 경고용 빨강 */
}
</style>