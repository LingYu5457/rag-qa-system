<script setup lang="ts">
import { ref } from 'vue'
import { useLoginForm } from '@/composables/useLogin'
import { useStatusStore } from '@/stores/statusStore'
import { useConversation } from '@/composables/useConversation'
import { useFile } from '@/composables/useFile'
import { login } from '@/api/auth'
import { ApiError } from '@/api/client'

const statusStore = useStatusStore()
const { loadSessions } = useConversation()
const { loadFiles } = useFile()
const loading = ref(false)
const apiError = ref('')

const { form, errors, touched, isValid, onBlur, onSubmit } = useLoginForm(
  async (data) => {
    apiError.value = ''
    loading.value = true
    try {
      const res = await login({
        user_account: data.account,
        user_password: data.password,
      })
      statusStore.setUser(res.data)
      await Promise.all([loadSessions(), loadFiles()])
    } catch (e) {
      apiError.value = e instanceof ApiError ? e.message : '登录失败，请稍后重试'
    } finally {
      loading.value = false
    }
  },
)
</script>

<template>
  <form class="login-form" @submit.prevent="onSubmit" novalidate>
    <h2 class="title">登录</h2>

    <div class="field">
      <label for="login-account">账号</label>
      <input
        id="login-account"
        v-model="form.account"
        type="text"
        autocomplete="username"
        placeholder="请输入账号"
        :class="{ error: touched.account && errors.account }"
        @blur="onBlur('account')"
      />
      <span v-if="touched.account && errors.account" class="err-msg">{{ errors.account }}</span>
    </div>

    <div class="field">
      <label for="login-password">密码</label>
      <input
        id="login-password"
        v-model="form.password"
        type="password"
        autocomplete="current-password"
        placeholder="请输入密码"
        :class="{ error: touched.password && errors.password }"
        @blur="onBlur('password')"
      />
      <span v-if="touched.password && errors.password" class="err-msg">{{ errors.password }}</span>
    </div>

    <p v-if="apiError" class="api-err-msg">{{ apiError }}</p>

    <button type="submit" :disabled="!isValid || loading" class="submit-btn">
      {{ loading ? '登录中...' : '登录' }}
    </button>
  </form>
</template>

<style scoped>
.login-form {
  width: 100%;
  max-width: 380px;
  margin: 0 auto;
  padding: 32px 28px;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
}

.title {
  margin: 0 0 28px;
  font-size: 22px;
  font-weight: 600;
  text-align: center;
  color: #1a1a1a;
}

.field {
  margin-bottom: 18px;
}

.field label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  color: #333;
}

.field input {
  width: 100%;
  padding: 10px 12px;
  font-size: 14px;
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.field input:focus {
  border-color: #4a90d9;
}

.field input.error {
  border-color: #e54d4d;
}

.err-msg {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: #e54d4d;
}

.submit-btn {
  width: 100%;
  margin-top: 8px;
  padding: 11px 0;
  font-size: 15px;
  font-weight: 500;
  color: #fff;
  background: #4a90d9;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:hover {
  background: #357abd;
}

.submit-btn:disabled {
  background: #b0cef0;
  cursor: not-allowed;
}

.api-err-msg {
  margin: 0 0 12px;
  padding: 8px 12px;
  font-size: 13px;
  color: #d43838;
  background: #fff0f0;
  border-radius: 6px;
  text-align: center;
}
</style>
