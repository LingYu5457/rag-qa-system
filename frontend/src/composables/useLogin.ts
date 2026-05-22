import { reactive, computed } from 'vue'

/* ======== 校验规则（与后端对齐） ======== */

const NAME_MAX = 15
const ACCOUNT_MAX = 20
const PASSWORD_MIN = 6
const PASSWORD_MAX = 20

function validateName(v: string): string {
  if (!v.trim()) return '请输入名称'
  if (v.trim().length > NAME_MAX) return `名称不能超过${NAME_MAX}个字符`
  return ''
}

function validateAccount(v: string): string {
  if (!v.trim()) return '请输入账号'
  if (v.trim().length > ACCOUNT_MAX) return `账号不能超过${ACCOUNT_MAX}个字符`
  return ''
}

function validatePassword(v: string): string {
  if (!v) return '请输入密码'
  if (v.length < PASSWORD_MIN) return `密码长度不能少于${PASSWORD_MIN}位`
  if (v.length > PASSWORD_MAX) return `密码长度不能超过${PASSWORD_MAX}位`
  return ''
}

function validateConfirmPassword(v: string, password: string): string {
  if (!v) return '请确认密码'
  if (v !== password) return '两次输入的密码不一致'
  return ''
}

/* ======== 登录表单 ======== */

export interface LoginFormState {
  account: string
  password: string
}

export function useLoginForm(
  onSuccess: (data: { account: string; password: string }) => void,
) {
  const form = reactive<LoginFormState>({
    account: '',
    password: '',
  })

  const errors = reactive({
    account: '',
    password: '',
  })

  const touched = reactive({
    account: false,
    password: false,
  })

  function validate() {
    errors.account = validateAccount(form.account)
    errors.password = validatePassword(form.password)
    return !errors.account && !errors.password
  }

  function onBlur(field: keyof typeof touched) {
    touched[field] = true
    if (field === 'account') errors.account = validateAccount(form.account)
    if (field === 'password') errors.password = validatePassword(form.password)
  }

  const isValid = computed(() => !validateAccount(form.account) && !validatePassword(form.password))

  function onSubmit() {
    Object.keys(touched).forEach((k) => (touched[k as keyof typeof touched] = true))
    if (!validate()) return
    onSuccess({ account: form.account.trim(), password: form.password })
  }

  return { form, errors, touched, isValid, onBlur, onSubmit }
}

/* ======== 注册表单 ======== */

export interface RegisterFormState {
  name: string
  account: string
  password: string
  confirmPassword: string
}

export function useRegisterForm(
  onSuccess: (data: { name: string; account: string; password: string }) => void,
) {
  const form = reactive<RegisterFormState>({
    name: '',
    account: '',
    password: '',
    confirmPassword: '',
  })

  const errors = reactive({
    name: '',
    account: '',
    password: '',
    confirmPassword: '',
  })

  const touched = reactive({
    name: false,
    account: false,
    password: false,
    confirmPassword: false,
  })

  function validate() {
    errors.name = validateName(form.name)
    errors.account = validateAccount(form.account)
    errors.password = validatePassword(form.password)
    errors.confirmPassword = validateConfirmPassword(form.confirmPassword, form.password)
    return !errors.name && !errors.account && !errors.password && !errors.confirmPassword
  }

  function onBlur(field: keyof typeof touched) {
    touched[field] = true
    switch (field) {
      case 'name':
        errors.name = validateName(form.name)
        break
      case 'account':
        errors.account = validateAccount(form.account)
        break
      case 'password':
        errors.password = validatePassword(form.password)
        if (touched.confirmPassword)
          errors.confirmPassword = validateConfirmPassword(form.confirmPassword, form.password)
        break
      case 'confirmPassword':
        errors.confirmPassword = validateConfirmPassword(form.confirmPassword, form.password)
        break
    }
  }

  const isValid = computed(
    () =>
      !validateName(form.name) &&
      !validateAccount(form.account) &&
      !validatePassword(form.password) &&
      !validateConfirmPassword(form.confirmPassword, form.password),
  )

  function onSubmit() {
    Object.keys(touched).forEach((k) => (touched[k as keyof typeof touched] = true))
    if (!validate()) return
    onSuccess({
      name: form.name.trim(),
      account: form.account.trim(),
      password: form.password,
    })
  }

  return { form, errors, touched, isValid, onBlur, onSubmit }
}
