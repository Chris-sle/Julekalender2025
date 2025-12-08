<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const password = ref('')

async function login() {
  if (!username.value || !password.value) {
    alert('Fyll inn både e-post og passord')
    return
  }

  const response = await fetch('http://localhost:5000/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: username.value,
      password: password.value
    })
  })

  if (!response.ok) {
    const err = await response.json()
    alert('Innlogging feilet: ' + err.message)
    return
  }

  // 🔥 Backend returnerer: { "access_token": "xxxx.yyyy.zzzz" }
  const data = await response.json()

  // 🔥 LAGRE TOKEN I LOCALSTORAGE
  localStorage.setItem('authToken', data.access_token)

  console.log("Token lagret:", data.access_token)

  // 🔥 ROUTE TIL ADMINPANELET
  router.push('/admin')
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-50 p-6">
    <div class="bg-gray-100 rounded-lg shadow-lg p-10 w-full max-w-md">

      <h1 class="text-2xl font-semibold mb-6 text-center">Logg inn</h1>

      <div class="mb-6">
        <label class="block mb-2 font-medium">E-post</label>
        <input
            v-model="username"
            type="email"
            placeholder="admin@test.no"
            class="w-full p-3 border rounded-md"
        />
      </div>

      <div class="mb-8">
        <label class="block mb-2 font-medium">Passord</label>
        <input
            v-model="password"
            type="password"
            placeholder="test"
            class="w-full p-3 border rounded-md"
        />
      </div>

      <button
          @click="login"
          class="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700">
        Logg inn
      </button>
    </div>
  </div>
</template>
