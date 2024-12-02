<template>
  <div class="pinset-board-container">
    <div class="board-header">
      <h2 class="board-title">
        <i class="mdi mdi-forum-outline mr-2"></i>
        FinSet 커뮤니티
      </h2>
      <button @click="goToCreatePost" class="create-post-btn">
        <i class="mdi mdi-plus"></i> 새 게시물
      </button>
    </div>

    <!-- 게시글 목록 -->
    <div v-if="posts.length > 0" class="post-list">
      <div 
        @click.prevent="viewPost(post.id)" 
        v-for="(post, index) in posts" 
        :key="post.id" 
        :class="['post-item', `post-variant-${index % 5}`]"
      >
        <div class="post-content">
          <h3 class="post-title">
            <i class="mdi mdi-file-document-outline mr-2"></i>
            {{ post.id }} 번째 글
          </h3>
          <p class="post-excerpt">{{ truncateContent(post.content) }}</p>
          <div class="post-meta">
            <div class="post-info">
              <span class="post-date">
                <i class="mdi mdi-calendar-outline mr-1"></i>
                {{ formatDate(post.created_at) }}
              </span>
              <span class="post-views">
                <i class="mdi mdi-eye-outline mr-1"></i>
                조회 {{ post.views || 1 }}
              </span>
            </div>
            <div class="post-tag">
              {{ getPostCategory(post) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 페이지 네비게이션 -->
    <div v-if="posts.length > 0" class="pagination">
      <button 
        :disabled="currentPage <= 1" 
        @click="getPosts(currentPage - 1)" 
        class="pagination-btn prev-btn"
      >
        <i class="mdi mdi-chevron-left"></i> 이전
      </button>
      <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
      <button 
        :disabled="currentPage >= totalPages" 
        @click="getPosts(currentPage + 1)" 
        class="pagination-btn next-btn"
      >
        다음 <i class="mdi mdi-chevron-right"></i>
      </button>
    </div>

    <!-- 게시글 없을 때 -->
    <div v-if="posts.length === 0" class="no-posts">
      <i class="mdi mdi-message-text-outline empty-icon"></i>
      <p>아직 게시된 글이 없습니다.</p>
      <button @click="goToCreatePost" class="create-first-post-btn">
        첫 게시물 작성하기
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      posts: [], 
      currentPage: 1, 
      totalPages: 1, 
      postCategories: [
        '투자', '금융', '재테크', '주식', '부동산', '보험', '세금'
      ]
    };
  },
  methods: {
    async getPosts(page = 1) {
      try {
        const response = await axios.get("http://127.0.0.1:8000/boards/", {
          params: { page },
        });
        this.posts = response.data.results;
        this.totalPages = response.data.total_pages;
        this.currentPage = response.data.current_page;
      } catch (err) {
        console.error("게시글을 불러오는 데 실패했습니다:", err);
      }
    },

    viewPost(postId) {
      this.$router.push({ name: "postDetail", params: { postId } });
    },
    
    goToCreatePost() {
      this.$router.push({ name: "createPost" });
    },

    truncateContent(content, maxLength = 100) {
      return content.length > maxLength 
        ? content.substring(0, maxLength) + '...' 
        : content;
    },

    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
    },

    getPostCategory(post) {
      // 랜덤 카테고리 선택 (실제 백엔드에서 카테고리를 제공한다면 그것을 사용)
      return this.postCategories[Math.floor(Math.random() * this.postCategories.length)];
    }
  },
  created() {
    this.getPosts();
  },
};
</script>

<style scoped>
:root {
  --primary-color: #2A6AC7;
  --secondary-color: #F5F7FA;
  --text-color: #333;
  --border-color: #E1E6EB;
}

.pinset-board-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

.post-list {
  margin-top: 20px;
}

.post-item {
  border-radius: 8px;
  margin-bottom: 15px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: all 0.3s ease;
}

.post-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* 다양한 포스트 변형 스타일 */
.post-variant-0 {
  background: linear-gradient(to right, #F6F9FC 98%, #3498DB 2%);
}
.post-variant-1 {
  background: linear-gradient(to right, #F6F9FC 98%, #2ECC71 2%);
}
.post-variant-2 {
  background: linear-gradient(to right, #F6F9FC 98%, #E74C3C 2%);
}
.post-variant-3 {
  background: linear-gradient(to right, #F6F9FC 98%, #F39C12 2%);
}
.post-variant-4 {
  background: linear-gradient(to right, #F6F9FC 98%, #9B59B6 2%);
}

.post-title {
  color: var(--primary-color);
  font-size: 1.1rem;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.post-excerpt {
  color: #666;
  margin-bottom: 10px;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #888;
  font-size: 0.9rem;
}

.post-info {
  display: flex;
  gap: 10px;
}

.post-tag {
  background-color: var(--primary-color);
  color: white;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

/* 나머지 스타일은 이전 코드와 동일 */
</style>