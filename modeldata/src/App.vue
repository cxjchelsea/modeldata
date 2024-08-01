

<template>
  <div>
    <login v-if="showLogin" @login-success="handleLoginSuccess"></login>
    <DaoHang v-if="showDaoHang" @logout="handleLogout" :isAdmin="isAdmin"></DaoHang>
  </div>
</template>

<script>
import DaoHang from '@/components/DaoHang.vue';
import Login from '@/components/LoginPage.vue';

export default {
  name: 'App',
  components: {
    DaoHang,
    Login,
  },

  data() {
    return {
      showDaoHang: false,
      isAdmin:false,
      showLogin: !localStorage.getItem('loggedIn'),
    };
  },
  created() {
    // 在应用启动时检查本地存储中的登录状态
    this.checkLoginStatus();
    console.log(localStorage)
  },
  methods: {
    checkLoginStatus() {
      const loggedIn = localStorage.getItem('loggedIn');
      if (loggedIn) {
        // 用户已登录，显示导航页面
        this.showDaoHang = true;
        this.showLogin = false;
        // 设置其他登录状态...
      } else {
        // 用户未登录，显示登录页面
        this.showDaoHang = false;
        this.showLogin = true;
      }
    },
    handleLogout() {
      this.showDaoHang = false;
      this.showLogin = true;
    },
    handleLoginSuccess(userData) {
      this.showDaoHang = true;
      this.showLogin = false;
      this.isAdmin = userData.role === 'admin';
      localStorage.setItem('loggedIn', 'true');
      this.checkLoginStatus();
    },
  },
}
</script>
