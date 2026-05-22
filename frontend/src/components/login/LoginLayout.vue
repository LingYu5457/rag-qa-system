<script setup lang="ts">
import { ref } from 'vue'
import LoginForm from './LoginForm.vue'
import RegistForm from './RegistForm.vue'

const mode = ref<'login' | 'register'>('login')
</script>

<template>
  <div class="login-layout">
    <div class="card">
      <LoginForm v-if="mode === 'login'" />
      <RegistForm v-else @registered="mode = 'login'" />

      <p class="switch-hint">
        <template v-if="mode === 'login'">
          还没有账号？
          <button class="link-btn" @click="mode = 'register'">立即注册</button>
        </template>
        <template v-else>
          已有账号？
          <button class="link-btn" @click="mode = 'login'">返回登录</button>
        </template>
      </p>
    </div>
  </div>
</template>

<style scoped>
.login-layout {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: #f5f6fa;
}

.card {
  width: 100%;
  max-width: 440px;
}

.switch-hint {
  margin-top: 20px;
  text-align: center;
  font-size: 13px;
  color: #888;
}

.link-btn {
  padding: 0;
  font-size: 13px;
  color: #4a90d9;
  background: none;
  border: none;
  cursor: pointer;
}

.link-btn:hover {
  text-decoration: underline;
}
</style>
