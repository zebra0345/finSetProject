<template>
  <v-container fluid class="chat-container pa-0 ma-0" style="height: 80vh;">
    <v-layout class="d-flex flex-column h-100">
      <!-- 헤더 -->
      <!-- <v-app-bar
        color="primary"
        dark
        elevation="2"
      >
        <v-avatar size="42" class="mr-3 bg-white">
          <v-icon color="primary" size="24">mdi-robot</v-icon>
        </v-avatar>
        
        <v-list-item
          class="pa-0"
          title="금융 도우미"
          subtitle="실시간 상담"
        >
          <template v-slot:append>
            <v-badge
              dot
              color="success"
              class="mr-3"
            ></v-badge>
          </template>
        </v-list-item>
      </v-app-bar> -->

    
      <v-app-bar color="primary" dark elevation="2">
        <v-avatar size="42" class="mr-3 bg-white">
          <v-icon color="primary" size="24">mdi-robot</v-icon>
        </v-avatar>
        
        <v-list-item
          class="pa-0"
          title="FINSET BOT"
          subtitle="실시간 상담"
        >
          <template v-slot:append>
            <v-badge dot color="success" class="mr-3"></v-badge>
          </template>
        </v-list-item>
      </v-app-bar>

      <!-- 메시지 영역 -->
      <v-main class="flex-grow-1 bg-grey-lighten-4">
        <v-container 
          ref="messageContainer"
          class="message-container py-4 px-4 overflow-y-auto"
          style="height: calc(100vh - 140px);"
        >
          <div
            v-for="(message, index) in messages"
            :key="message.id"
            class="message-wrapper mb-4"
          >
            <div 
              class="d-flex message-bubble"
              :class="message.type === 'user' ? 'justify-end' : 'justify-start'"
            >
              <!-- 봇 아바타 -->
              <v-avatar
                v-if="message.type === 'bot'"
                size="36"
                class="mr-2 mt-1"
              >
                <v-icon color="primary">mdi-robot</v-icon>
              </v-avatar>

              <div class="message-content" :class="message.type === 'user' ? 'user-message' : 'bot-message'">
                <v-card
                  :color="message.type === 'user' ? 'primary' : 'white'"
                  :class="message.type === 'user' ? 'user-bubble' : 'bot-bubble'"
                  elevation="1"
                  class="message-card"
                >
                  <v-card-text 
                    :class="[
                      message.type === 'user' ? 'text-white' : 'text-black',
                      'pa-3'
                    ]"
                  >
                    <!-- 사용자 메시지는 그대로 표시 -->
                    <template v-if="message.type === 'user'">
                      {{ message.text }}
                    </template>
                    
                    <!-- 봇 메시지는 마크다운 렌더링 -->
                    <div 
                      v-else 
                      class="markdown-body"
                      v-html="message.renderedText"
                    ></div>
                  </v-card-text>
                </v-card>
                
                <div 
                  v-if="message.timestamp"
                  class="message-time text-caption text-grey"
                  :class="message.type === 'user' ? 'text-right' : 'text-left'"
                >
                  {{ formatTime(message.timestamp) }}
                </div>
              </div>

              <!-- 사용자 아바타 -->
              <v-avatar
                v-if="message.type === 'user'"
                size="36"
                class="ml-2 mt-1"
              >
                <v-icon>mdi-account</v-icon>
              </v-avatar>
            </div>
          </div>
        </v-container>
      </v-main>

      <!-- 입력 영역 -->
      <v-footer class="pa-4 bg-white" elevation="4">
        <v-row no-gutters align="center">
          <v-col>
            <v-text-field
              v-model="userInput"
              placeholder="메시지를 입력하세요..."
              append-inner-icon="mdi-send"
              variant="outlined"
              density="comfortable"
              hide-details
              @click:append-inner="sendMessage"
              @keyup.enter="sendMessage"
              class="message-input"
              :loading="isLoading"
              :disabled="isLoading"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-footer>
    </v-layout>

    <!-- 에러 알림 -->
    <v-snackbar
      v-model="showError"
      color="error"
      :timeout="3000"
    >
      오류가 발생했습니다. 잠시 후 다시 시도해주세요.
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

// marked 설정
marked.setOptions({
  breaks: true,  // 줄바꿈 활성화
  gfm: true      // GitHub Flavored Markdown 활성화
});

const messageContainer = ref(null);
const userInput = ref('');
const isLoading = ref(false);
const showError = ref(false);

// 마크다운을 안전한 HTML로 변환하는 함수
const convertMarkdownToSafeHtml = (markdown) => {
  try {
    // 마크다운을 HTML로 변환
    const rawHtml = marked(markdown);
    // HTML 살균 (XSS 방지)
    const sanitizedHtml = DOMPurify.sanitize(rawHtml);
    return sanitizedHtml;
  } catch (error) {
    console.error('Markdown conversion error:', error);
    return markdown;
  }
};

// 메시지 초기값 설정
const messages = ref([
  { 
    id: 1, 
    type: 'bot',
    text: '안녕하세요! 금융 상담을 도와드릴 수 있어 기쁩니다.\n\n**어떤 도움이 필요하신가요?**',
    renderedText: convertMarkdownToSafeHtml('안녕하세요! 금융 상담을 도와드릴 수 있어 기쁩니다.\n\n**어떤 도움이 필요하신가요?**'),
    timestamp: new Date() 
  }
]);

// 시간 포맷 함수
const formatTime = (date) => {
  return new Date(date).toLocaleTimeString('ko-KR', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  });
};

// 메시지 영역 자동 스크롤
const scrollToBottom = () => {
  if (messageContainer.value) {
    setTimeout(() => {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
    }, 100);
  }
};

// 메시지 추가될 때마다 스크롤
watch(messages, () => {
  scrollToBottom();
}, { deep: true });

// 메시지 전송
const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return;
  
  // 사용자 메시지 추가
  messages.value.push({
    id: messages.value.length + 1,
    type: 'user',
    text: userInput.value,
    timestamp: new Date()
  });

  isLoading.value = true;

  try {
    const response = await fetch('http://127.0.0.1:8000/chatBots/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: userInput.value })
    });
    
    if (!response.ok) throw new Error('API 호출 실패');
    
    const data = await response.json();
    
    // 봇 응답 메시지 추가 (마크다운 변환 적용)
    messages.value.push({
      id: messages.value.length + 1,
      type: 'bot',
      text: data.result,
      renderedText: convertMarkdownToSafeHtml(data.result),
      timestamp: new Date()
    });
  } catch (error) {
    console.error('Error:', error);
    showError.value = true;
    const errorMessage = '죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
    messages.value.push({
      id: messages.value.length + 1,
      type: 'bot',
      text: errorMessage,
      renderedText: convertMarkdownToSafeHtml(errorMessage),
      timestamp: new Date()
    });
  } finally {
    isLoading.value = false;
    userInput.value = '';
  }
};

onMounted(() => {
  scrollToBottom();
});
</script>

<style>
/* 마크다운 스타일링 */
.markdown-body {
  line-height: 1.6;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4 {
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.markdown-body p {
  margin-bottom: 0.5em;
}

.markdown-body ul,
.markdown-body ol {
  padding-left: 1.5em;
  margin-bottom: 0.5em;
}

.markdown-body li {
  margin-bottom: 0.25em;
}

.markdown-body code {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: monospace;
}

.markdown-body pre {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 1em;
  border-radius: 4px;
  overflow-x: auto;
  margin: 0.5em 0;
}

.markdown-body blockquote {
  border-left: 4px solid #ddd;
  padding-left: 1em;
  margin: 0.5em 0;
  color: #666;
}

.markdown-body strong {
  font-weight: 600;
}

.markdown-body em {
  font-style: italic;
}

/* 기존 스타일 유지 */
.message-container {
  scroll-behavior: smooth;
}

.message-bubble {
  margin-bottom: 8px;
}

.message-card {
  max-width: 80%;
  border-radius: 16px !important;
}

.user-bubble {
  border-bottom-right-radius: 4px !important;
}

.bot-bubble {
  border-bottom-left-radius: 4px !important;
}

.message-time {
  margin-top: 4px;
  font-size: 0.75rem;
}

.message-container::-webkit-scrollbar {
  width: 6px;
}

.message-container::-webkit-scrollbar-track {
  background: transparent;
}

.message-container::-webkit-scrollbar-thumb {
  background: #E0E0E0;
  border-radius: 3px;
}

.message-container::-webkit-scrollbar-thumb:hover {
  background: #BDBDBD;
}

.message-input :deep(.v-field__outline__start) {
  border-radius: 24px 0 0 24px !important;
}

.message-input :deep(.v-field__outline__end) {
  border-radius: 0 24px 24px 0 !important;
}
</style>