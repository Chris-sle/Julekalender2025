<script setup>
import {ref, onUnmounted} from "vue";

let selectedDay = ref(null)
let theText = ref(null)

const files = ref([]);
const previews = ref({});

const onFileChange = (event) => {
  const newFiles = Array.from(event.target.files);
  newFiles.forEach(file => {
    files.value.push(file);
    if (isImage(file) || isVideo(file)) {
      previews.value[file.name] = URL.createObjectURL(file);
    }
  });
  event.target.value = '';
};

const formatBytes = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const isImage = (file) => file.type.startsWith('image/');
const isVideo = (file) => file.type.startsWith('video/');


const save = async () => {
  if (!selectedDay.value || !theText.value?.trim() || files.value.length === 0) {
    alert('Vennligst velg dag, skriv tekst og last opp minst én fil.');
    return;
  }

  const formData = new FormData();
  formData.append('task_text', theText.value);
  files.value.forEach(file => formData.append('files', file));

  try {
    const token = localStorage.getItem('authToken');
    const response = await fetch(`/api/calendar/${selectedDay.value}`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: formData
    });

    if (!response.ok) throw new Error('Upload feilet');
    const data = await response.json();
    console.log('Lagt til:', data);

    files.value = [];
    previews.value = {};
    theText.value = '';
    alert('Lagret!');

  } catch (error) {
    console.error('Feil:', error);
    alert('Feil ved lagring: ' + error.message);
  }
};

onUnmounted(() => Object.values(previews.value).forEach(URL.revokeObjectURL));

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

      <button @click="save" class="mt-6 w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200">Lagre</button>
    </div>
  </div>
</template>

<style scoped>
</style>
