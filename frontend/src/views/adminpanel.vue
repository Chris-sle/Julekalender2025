<script setup>
import {ref} from "vue";

let selectedDay = ref(null)
let theText = ref(null)

const test =  () => {
  console.log(theText.value)
}
</script>

<template>
  <div class="flex-1 grid grid-cols-2 md:grid-cols-2 gap-10 p-6 bg-gray-50 ">
    <div class="col-span-full">
      <h1 class="text-3xl font-bold text-gray-900 mb-8 bg-blue-100 text-center">Admin - Julekalender</h1>
    </div>

    <div class="bg-gray-100 rounded-lg shadow-lg p-10">
      <label class="block mb-2 text-sm font-medium text-gray-700">Velg dag</label>
      <select v-model="selectedDay" class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500" required>
        <option v-for="day in 24" :key="day" :value="day">{{ day }}. desember</option>
      </select>

      <div>
        <label for="text" class="block mb-2 text-sm font-medium text-gray-700">Tekst for luke {{ selectedDay }}:</label>
        <textarea
            v-model="theText"
            id="text"
            placeholder="Skriv inn tekst her..."
            class="w-full h-full p-3 border border-gray-300 rounded-md resize-vertical min-h-[120px] focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            required
        ></textarea>
      </div>
    </div>

    <div class="bg-gray-100 rounded-lg shadow-lg p-6">


      <div class="mt-6">
        <label class="block mb-2 text-sm font-medium text-gray-700">Last opp filer</label>
        <input
            class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 mb-4"
            type="file"
            @change="onFileChange"
            accept="image/*,video/*,.pdf,.docx"
            multiple
        />

        <div v-for="file in files" :key="file.name" class="border border-gray-200 rounded-md p-3 bg-gray-50 mb-4">
          <p class="text-sm text-gray-600 mb-2">{{ file.name }} ({{ formatBytes(file.size) }})</p>
          <img v-if="isImage(file)" :src="previews[file.name]" class="max-w-full h-32 object-cover rounded" />
          <video v-if="isVideo(file)" :src="previews[file.name]" controls class="max-w-full h-32 rounded"></video>
        </div>
      </div>

      <button @click="test" class="mt-6 w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200">Lagre</button>
    </div>
  </div>
</template>

<style scoped>
</style>
