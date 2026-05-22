<script setup lang="ts">
import { ref } from 'vue'
import { useRegisterForm } from '@/composables/useLogin'
import { register } from '@/api/auth'
import { ApiError } from '@/api/client'

const emit = defineEmits<{
  registered: []
}>()

const loading = ref(false)
const apiError = ref('')

const { form, errors, touched, isValid, onBlur, onSubmit } = useRegisterForm(
  async (data) => {
    apiError.value = ''
    loading.value = true
    try {
      await register({
        user_name: data.name,
        user_account: data.account,
        user_password: data.password,
      })
      alert('注册成功，请登录')
      emit('registered')
    } catch (e) {
      apiError.value = e instanceof ApiError ? e.message : '注册失败，请稍后重试'
    } finally {
      loading.value = false
    }
  },
)
</script>

<template>
  <form class="regist-form" @submit.prevent="onSubmit" novalidate>
    <h2 class="title">注册</h2>

    <div class="field">
      <label for="regist-name">名称</label>
      <input
        id="regist-name"
        v-model="form.name"
        type="text"
        autocomplete="nickname"
        placeholder="请输入名称"
        :class="{ error: touched.name && errors.name }"
        @blur="onBlur('name')"
      />
      <span v-if="touched.name && errors.name" class="err-msg">{{ errors.name }}</span>
    </div>

    <div class="field">
      <label for="regist-account">账号</label>
      <input
        id="regist-account"
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
      <label for="regist-password">密码</label>
      <input
        id="regist-password"
        v-model="form.password"
        type="password"
        autocomplete="new-password"
        placeholder="请输入密码"
        :class="{ error: touched.password && errors.password }"
        @blur="onBlur('password')"
      />
      <span v-if="touched.password && errors.password" class="err-msg">{{ errors.password }}</span>
    </div>

    <div class="field">
      <label for="regist-confirm-password">确认密码</label>
      <input
        id="regist-confirm-password"
        v-model="form.confirmPassword"
        type="password"
        autocomplete="new-password"
        placeholder="请再次输入密码"
        :class="{ error: touched.confirmPassword && errors.confirmPassword }"
        @blur="onBlur('confirmPassword')"
      />
      <span v-if="touched.confirmPassword && errors.confirmPassword" class="err-msg">{{ errors.confirmPassword }}</span>
    </div>

    <p v-if="apiError" class="api-err-msg">{{ apiError }}</p>

    <button type="submit" :disabled="!isValid || loading" class="submit-btn">
      {{ loading ? '注册中...' : '注册' }}
    </button>
  </form>
</template>

<style scoped>
.regist-form {
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
