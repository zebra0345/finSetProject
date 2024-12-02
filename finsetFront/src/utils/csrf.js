// utils/csrf.js 파일 예시
export function getCSRFToken() {
  const csrfCookie = document.cookie
    .split(";")
    .find(cookie => cookie.trim().startsWith("csrftoken="));
  
  return csrfCookie ? csrfCookie.split("=")[1] : null;
}