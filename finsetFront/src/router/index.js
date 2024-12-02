import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/accounts/LoginView.vue'
import SignUpView from '@/views/accounts/SignUpView.vue'
import FindpasswordView from '@/views/accounts/FindpasswordView.vue'
import MapView from '@/views/kakao/MapView.vue'
import ProductsView from '@/views/Products/ProductsView.vue'
import ProductItemView from '@/views/Products/ProductItemView.vue'
import ProfileView from '@/views/accounts/ProfileView.vue'
import ExchangesVIew from '@/views/exchanges/ExchangesVIew.vue'
import BoardListView from '@/views/boards/BoardListView.vue'
import CreateBoardView from '@/views/boards/CreateBoardView.vue'
import PostDetailView from '@/views/boards/PostDetailView.vue'
import ModifyView from '@/views/accounts/ModifyView.vue'
import ChatBotsView from '@/views/chatbots/ChatBotsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 메인페이지
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    // 로그인페이지
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    // 회원가입
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
    },
    { path: "/findpassword",
      name: "findpassword", 
      component: FindpasswordView,
    },
    {
      path:'/searchMap',
      name:'searchMap',
      component: MapView,
    },
    {
      path:'/products',
      name:'products',
      component: ProductsView,
    },
    {
      path: "/product/:id",
      name: "product-detail",
      component: ProductItemView,
      props:true,
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/exchanges',
      name: 'exchanges',
      component: ExchangesVIew,
    },
    {
      path: '/boards',
      name: 'boards',
      component: BoardListView,
    },
    {
      path: '/createPost',
      name: 'createPost',
      component: CreateBoardView,
    },
    { path: '/post/:postId', 
      name: 'postDetail', 
      component: PostDetailView 
    },
    { path: '/modify', 
      name: 'modify', 
      component: ModifyView 
    },
    { path: '/chatbot', 
      name: 'chatbot', 
      component: ChatBotsView 
    },


  ],
})

export default router
