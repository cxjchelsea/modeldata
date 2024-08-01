<!-- LoginPage.vue -->
<template>
    <div class="back">
      <h1>板带轧制基础模型库/生产数据库</h1>
      <div class="login">
        <form @submit.prevent="login">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="username" :placeholder="placeholderOne" required>
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" :placeholder="placeholderTwo" required>
          <button type="submit">Login</button>
      </form>
      </div>
    </div>
  </template>
  
  <script>
  import {LOGIN} from '@/config'
  
  export default {
    name: 'HomePage',
    data() {
      return {
        username: '',
        password: '',
        placeholderOne: '请输入账户名称',
        placeholderTwo: '请输入账号密码',
      };
    },
    methods: {
      async login() {
        try {
          const response = await fetch(LOGIN, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password,
            }),
          });
  
          if (response.ok) {
            const data = await response.json();
            console.log('Login successful');
            console.log('User Role:', data.role);
            this.$emit('login-success', data);
            localStorage.setItem('isLoggedIn', true);
          } else {
            this.username='';
            this.password='';
            console.error('Login failed:', response.statusText);
            // 弹出提示框
            window.alert('Username or password is incorrect. Please try again.');
          }
        } catch (error) {
          console.error('Login failed:', error.message);
          // 弹出提示框
          window.alert('An error occurred during login. Please try again.');
        }
      },
    },
  };
  </script>
  <style>
  .back {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('./home.jpg');
    background-size: cover;
    background-repeat: no-repeat;
  }
  
  .back h1 {
    position: absolute;
    top: 30%;
    left: 50%;
    transform: translate(-100%, 30%);
    color: rgb(255, 255, 255);
    font-size: 40px;
  }
  .login{
    background-color: #1f80e0;
    width: 35%;
    height: 70%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(20%, -50%);
  }
  .login form {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
  }
  .login form input{
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-bottom: 5%;
    width: 60%;
    height: 8%;
  }
  .login form button{
    border: none;
    background-color: #4caf50;
    color: #fff;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    width: 60%;
    height: 8%;
  }
  </style>