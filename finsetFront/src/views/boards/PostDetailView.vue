<template>
  <div class="post-detail-container">
    <div v-if="post" class="post-detail">
      <!-- 게시글 제목 -->
      <h1 v-if='post.comments.length>0' class="post-content">{{ post.results[0].board.content }}</h1>
      <h1 v-else class="post-content">{{ post.results.content }}</h1>

      <!-- 게시글 삭제 버튼 -->
        <button
          v-if="post.results[0] && post.results[0].board.User.id === currentUserId"
          @click="deletePost"
          class="btn delete-post-btn"
        >
          게시글 삭제
        </button>


      <hr />

      <!-- 댓글 목록 -->
      <div class="comments-section">
        <h3>댓글</h3>
        <div v-if="post.comments && post.comments.length > 0" class="comment-list">
          <div
            v-for="comment in post.comments"
            :key="comment.id"
            class="comment-item"
          >
            <p class="comment-content">{{ comment.content }}</p>
            <p class="comment-author">작성자: 사용자 {{ comment.User.id }}</p>
            <p class="comment-created">작성일: {{ formatDate(comment.created_at) }}</p>

            <!-- 댓글 삭제 버튼 (작성자만) -->
            <button
              v-if="comment.User.id === currentUserId"
              @click="deleteComment(comment.id)"
              class="btn delete-comment-btn"
            >
              댓글 삭제
            </button>
          </div>
        </div>
        <p v-else class="no-comments">댓글이 없습니다.</p>
      </div>

      <hr />

      <!-- 댓글 작성 폼 -->
      <div class="comment-form">
        <textarea
          v-model="newComment"
          placeholder="댓글을 입력하세요..."
          class="comment-input"
        ></textarea>
        <button @click="addComment" class="btn comment-btn">댓글 작성</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      post: null, // 선택된 게시글 데이터
      newComment: "", // 새 댓글 내용
      currentUserId: null, // 현재 로그인한 사용자 ID
    };
  },
  methods: {
    // 게시글 상세 조회
    async getPostDetail(postId) {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/boards/${postId}/`
        );
        this.post = response.data; // 게시글과 댓글을 포함한 데이터
        this.post.comments = response.data.results; // 댓글을 추출하여 저장
        console.log(this.post.results[0].board.User.id)
        console.log(this.post)
        // 현재 로그인한 사용자 ID 확인
        const userToken = localStorage.getItem('community');
        if (userToken) {
          const tokenData = JSON.parse(userToken);
          this.currentUserId = tokenData.user.pk; // 로그인한 사용자 ID
        }
      } catch (err) {
        console.error(err);
      }
    },

    // 댓글 삭제
    async deleteComment(commentId) {
      if (confirm("댓글을 삭제하시겠습니까?")) {
        try {
          const userToken = localStorage.getItem('community');
          const token = JSON.parse(userToken).token;
          
          await axios.delete(
            `http://127.0.0.1:8000/boards/comment/${commentId}/`,
            {
              headers: {
                Authorization: `Token ${token}`, // 헤더에 토큰 추가
              },
            }
          );

          this.getPostDetail(this.$route.params.postId); // 댓글 삭제 후 게시글 다시 불러오기
        } catch (err) {
          console.error(err);
        }
      }
    },

          // 게시글 삭제 메서드
      async deletePost() {
        if (confirm("게시글을 삭제하시겠습니까?")) {
          try {
            const userToken = localStorage.getItem('community');
            const token = JSON.parse(userToken).token;

            await axios.delete(
              `http://127.0.0.1:8000/boards/${this.$route.params.postId}/`,
              {
                headers: {
                  Authorization: `Token ${token}`,
                },
              }
            );

            alert("게시글이 삭제되었습니다.");
            this.$router.push("/boards"); // 게시판 목록으로 이동
          } catch (err) {
            console.error(err);
            alert("게시글 삭제에 실패했습니다.");
          }
        }
      },


    // 댓글 추가
    async addComment() {
      if (!this.newComment) {
        alert("댓글 내용을 입력해주세요.");
        return;
      }

      try {
        const userToken = localStorage.getItem('community');
        const token = JSON.parse(userToken).token;

        await axios.post(
          `http://127.0.0.1:8000/boards/${this.$route.params.postId}/`,
          { content: this.newComment },
          {
            headers: {
              Authorization: `Token ${token}`, // 헤더에 토큰 추가
            },
          }
        );

        this.newComment = ""; // 댓글 작성 후 초기화
        this.getPostDetail(this.$route.params.postId); // 댓글 추가 후 게시글 다시 불러오기
      } catch (err) {
        console.error(err);
      }
    },

    // 날짜 포맷 함수
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString(); // '2024-11-21T07:23:24.048813Z' 형식을 보기 좋게 변환
    },
  },
  created() {
    const postId = this.$route.params.postId; // URL 파라미터에서 postId 가져오기
    if (!postId) {
      console.error("postId가 없습니다. URL을 확인하세요.");
      return;
    }
    this.getPostDetail(postId); // 게시글 상세 정보 요청
  },
};

</script>

<style scoped>
.delete-post-btn {
  background-color: #ff6f61;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
}

.delete-post-btn:hover {
  background-color: #ff4c3b;
}

/* 기존 스타일 유지 */
.post-detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.post-title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

.post-content {
  font-size: 1.2rem;
  line-height: 1.6;
  color: #555;
  margin-bottom: 20px;
}

.comments-section {
  margin-top: 30px;
}

.comment-list {
  margin-top: 10px;
}

.comment-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.comment-content {
  font-size: 1rem;
  color: #444;
}

.no-comments {
  font-size: 1rem;
  color: #888;
  text-align: center;
}

.comment-form {
  margin-top: 20px;
}

.comment-input {
  width: 100%;
  height: 80px;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  font-size: 1rem;
  margin-bottom: 10px;
  resize: none;
}

.btn {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

/* 댓글 작성 버튼 스타일 */
.comment-btn {
  background-color: #007bff;
  color: white;
}

.comment-btn:hover {
  background-color: #0056b3;
}

/* 댓글 삭제 버튼 스타일 개선 */
.delete-comment-btn {
  background-color: #ff6f61; /* 부드러운 빨간색 */
  color: white;
  font-size: 1rem;
  padding: 8px 16px;
  border-radius: 25px;
  border: 2px solid #ff6f61;
  transition: all 0.3s ease; /* 부드러운 전환 효과 */
}

.delete-comment-btn:hover {
  background-color: white;
  color: #ff6f61;
  transform: translateY(-2px); /* 버튼이 살짝 위로 올라오는 효과 */
}

.delete-comment-btn:active {
  transform: translateY(1px); /* 클릭 시 살짝 내려가는 효과 */
}
</style>
