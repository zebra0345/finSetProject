<template>
  <div class="create-post-container">
    <div class="create-post-card">
      <div class="create-post-header">
        <Landmark class="header-icon" strokeWidth={2.5} />
        <h2 class="create-post-title">금융 정보 공유하기</h2>
      </div>
      
      <form @submit.prevent="createPost" class="form-wrapper">
        <div class="input-group">
          <div class="input-label" :class="{ 'has-value': newPost.title }">
            <BookText class="label-icon" />
            <label>제목</label>
          </div>
          <div class="input-container">
            <input 
              v-model="newPost.title" 
              placeholder="어떤 금융 정보를 공유하고 싶으신가요?" 
              class="input-field" 
              :class="{ 'is-filled': newPost.title }"
              type="text"
            />
            <span class="input-border"></span>
          </div>
        </div>
        
        <div class="input-group">
          <div class="input-label" :class="{ 'has-value': newPost.content }">
            <ScrollText class="label-icon" />
            <label>내용</label>
          </div>
          <div class="input-container">
            <textarea 
              v-model="newPost.content" 
              placeholder="상세한 정보나 팁을 자유롭게 작성해주세요" 
              class="input-field content-field"
              :class="{ 'is-filled': newPost.content }"
            ></textarea>
            <span class="input-border"></span>
          </div>
        </div>

        <div class="button-group">
          <button type="button" class="cancel-btn" @click="$router.push('/boards/')">
            <X class="button-icon" />
            취소하기
          </button>
          <button 
            type="submit" 
            class="create-btn"
            :disabled="!newPost.title || !newPost.content"
          >
            <Share2 class="button-icon" />
            공유하기
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';
import { Landmark, BookText, ScrollText, Share2, X } from 'lucide-vue-next';

export default {
  components: {
    Landmark,
    BookText,
    ScrollText,
    Share2,
    X
  },
  data() {
    return {
      newPost: { 
        title: '', 
        content: '' 
      },
    };
  },
  methods: {
    async createPost() {
      if (!this.newPost.title || !this.newPost.content) {
        alert("제목과 내용을 모두 입력해주세요.");
        return;
      }

      try {
        const userToken = ref(localStorage.getItem('community'));
        const token = JSON.parse(userToken.value).token;
        await axios.post('http://127.0.0.1:8000/boards/', this.newPost, {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        this.$router.push('/boards/');
      } catch (err) {
        console.error(err);
        alert("게시글 작성 중 오류가 발생했습니다.");
      }
    },
  },
};
</script>

<style scoped>
.create-post-container {
  min-height: 100vh;
  padding: 2rem;
  background-color: #f8fafc;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.create-post-card {
  width: 100%;
  max-width: 800px;
  background: white;
  border-radius: 24px;
  padding: 2.5rem;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
}

.create-post-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 3rem;
}

.header-icon {
  width: 40px;
  height: 40px;
  color: #2563eb;
}

.create-post-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.form-wrapper {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-weight: 500;
  transition: color 0.2s;
}

.input-label.has-value {
  color: #2563eb;
}

.label-icon {
  width: 20px;
  height: 20px;
}

.input-container {
  position: relative;
}

.input-field {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background: white;
  transition: all 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 4px rgb(37 99 235 / 0.1);
}

.input-field.is-filled {
  border-color: #2563eb;
}

.content-field {
  min-height: 250px;
  resize: vertical;
  line-height: 1.6;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.create-btn, .cancel-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.2s;
}

.create-btn {
  background-color: #2563eb;
  color: white;
  border: none;
}

.create-btn:hover:not(:disabled) {
  background-color: #1d4ed8;
  transform: translateY(-1px);
}

.create-btn:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}

.cancel-btn {
  background-color: #f1f5f9;
  color: #64748b;
  border: none;
}

.cancel-btn:hover {
  background-color: #e2e8f0;
  color: #475569;
}

.button-icon {
  width: 20px;
  height: 20px;
}

@media (max-width: 768px) {
  .create-post-container {
    padding: 1rem;
  }
  
  .create-post-card {
    padding: 1.5rem;
  }
  
  .create-post-title {
    font-size: 1.5rem;
  }
  
  .button-group {
    flex-direction: column;
  }
  
  .create-btn, .cancel-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>