<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();


const token = ref(null);
const selectedDay = ref(null);
const theText = ref("");
const files = ref([]);
const previews = ref({});
let theSavedFiles = ref({});

const isImage = (file) => file.type.startsWith('image/');
const isVideo = (file) => file.type.startsWith('video/');


onMounted(() => {
  token.value = localStorage.getItem("authToken");

  console.log("Token:", token.value);

  if (!token.value) {
    return router.push("/login");
  }
});


const dateStr = computed(() => {
  if (!selectedDay.value) return null;
  return `2025-12-${String(selectedDay.value).padStart(2, "0")}`;
});


function onFileChange(event) {
  const incoming = Array.from(event.target.files);

  incoming.forEach((file) => {
    files.value.push(file);
    previews.value[file.name] = URL.createObjectURL(file);
  });

  event.target.value = "";
}

onUnmounted(() => {
  Object.values(previews.value).forEach(URL.revokeObjectURL);
});


function formatBytes(bytes) {
  const units = ["Bytes", "KB", "MB", "GB"];
  if (!bytes) return "0 Bytes";
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return (bytes / Math.pow(1024, i)).toFixed(2) + " " + units[i];
}

// --------------------
// GET ENTRY FOR TESTING
// --------------------
async function getAllData() {
  if (!dateStr.value) return alert("Velg en dag først");

  const response = await fetch(
      `http://127.0.0.1:5000/calendar/${dateStr.value}`,
      {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      }
  );

  if (response.status === 401) {
    alert("Logg inn på nytt");
    return router.push("/admin");
  }

  theSavedFiles.value =  await response.json();
}

// --------------------
// SAVE ENTRY WITH FILES
// --------------------
async function save() {
  if (!dateStr.value || !theText.value.trim() || files.value.length === 0) {
    return alert("Fyll ut alle felter og last opp fil");
  }

  const formData = new FormData();
  formData.append("date", dateStr.value);
  formData.append("task_text", theText.value);
  formData.append("video_type", "upload");
  formData.append("is_published", "true");

  files.value.forEach((file) => formData.append("files", file));

  const response = await fetch("http://127.0.0.1:5000/calendar", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token.value}`,
    },
    body: formData,
  });

  if (response.status === 401) {
    alert("Token utløpt, logg inn igjen");
    return router.push("/admin-login");
  }

  if (!response.ok) {
    console.error(await response.text());
    return alert("Upload feilet.");
  }

  console.log("LAGRET:", await response.json());

  // Reset
  selectedDay.value = null;
  theText.value = "";
  files.value = [];
  previews.value = {};

  alert("Lagret!");
}
</script>


<template>
  <div class="flex-1 grid grid-cols-2 md:grid-cols-2 gap-10 p-6 bg-gray-50 ">
    <div class="col-span-full">
      <h1 class="text-3xl font-bold text-gray-900 mb-8 bg-blue-100 text-center">Admin - Julekalender</h1>
    </div>

    <div class="bg-gray-100 rounded-lg shadow-lg p-10">
      <label class="block mb-2 text-sm font-medium text-gray-700">Velg dag</label>
      <select v-model="selectedDay" class="w-full p-3 border border-gray-300 rounded-md" required>
        <option v-for="day in 24" :key="day" :value="day">{{ day }}. desember</option>
      </select>

      <div class="mt-4">
        <label class="block mb-2 text-sm font-medium text-gray-700">
          Tekst for luke {{ selectedDay }}:
        </label>
        <textarea
            v-model="theText"
            class="w-full h-full p-3 border border-gray-300 rounded-md min-h-[120px]"
            placeholder="Skriv tekst..."
            required
        ></textarea>
      </div>
    </div>

    <div class="bg-gray-100 rounded-lg shadow-lg p-6">
      <label class="block mb-2 text-sm font-medium text-gray-700">Last opp filer</label>

      <input
          class="w-full p-2 border border-gray-300 rounded-md mb-4"
          type="file"
          @change="onFileChange"
          accept="image/*,video/*,.pdf,.docx"
          multiple
      />

      <div
          v-for="file in files"
          :key="file.name"
          class="border border-gray-200 rounded-md p-3 bg-gray-50 mb-4"
      >
        <p class="text-sm text-gray-600 mb-2">
          {{ file.name }} ({{ formatBytes(file.size) }})
        </p>
        <img v-if="isImage(file)" :src="previews[file.name]" class="h-32 object-cover rounded" />
        <video v-if="isVideo(file)" :src="previews[file.name]" controls class="h-32 rounded"></video>
      </div>

      <button @click="save" class="mt-6 w-full bg-blue-600 text-white py-3 rounded-md">
        Lagre
      </button>

      <button @click="getAllData" class="mt-3 w-full bg-green-600 text-white py-3 rounded-md">
        Klikk her for info
      </button>
      {{ theSavedFiles.video_path }}
    </div>
  </div>
</template>

