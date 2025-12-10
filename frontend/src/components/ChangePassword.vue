<template>
    <div class="bg-white rounded-1g shadow-md p-6 max-w-md w-full">
        <h2 class="text-xl font-bold text-gray-800 mb-4 border-b pb-2">Endre Passord</h2>

        <div class="space-y-4">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nytt passord</label>
                <input v-model="newPassword" type="password" placeholder="••••••••"
                    class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none" />
            </div>

            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Bekreft passord</label>
                <input v-model="confirmPassword" type="password" placeholder="••••••••"
                    class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none" />
            </div>

            <div v-if="message"
                :class="['p-3 rounded-md text-sm', isError ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700']">
                {{ message }}
            </div>

            <button @click="changePassword" :disabled="isLoading"
                class="w-full bg-gray-800 text-white py-2 px-4 rounded-md hover:bg-gray-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium">
                {{ isLoading ? "Lagrer..." : "Oppdater passord" }}
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const newPassword = ref('');
const confirmPassword = ref('');
const isLoading = ref(false);
const message = ref('');
const isError = ref(false);

async function changePassword() {
    message.value = '';
    isError.value = false;

    // Enkel validering
    if (!newPassword.value) {
        message.value = 'Vennligst fyll inn begge feltene.';
        isError.value = true;
        return;
    }

    if (newPassword.value !== confirmPassword.value) {
        message.value = 'Passordene er ikke like.';
        isError.value = true;
        return;
    }

    const token = localStorage.getItem('authToken');
    if (!token) {
        alert("Du må være logget inn.");
        return router.push("/login");
    }

    isLoading.value = true;

    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/auth/change-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ new_password: newPassword.value })
        });

        const data = await response.json();

        if (response.ok) {
            message.value = "Passordet ble endret!";
            newPassword.value = "";
            confirmPassword.value = "";
        } else {
            isError.value = true;
            message.value = data.message || "Noe gikk galt.";

            // Hvis token har utløpt, kast til login
            if (response.status === 401) {
                setTimeout(() => router.push("/login"), 1500);
            }
        }
    } catch (error) {
        isError.value = true;
        message.value = "Kunne ikke koble til serveren.";
        console.error(error);
    } finally {
        isLoading.value = false;
    }
}
</script>