<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import ChangePassword from "../components/ChangePassword.vue";

const router = useRouter();

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

const token = ref(null);
const selectedDay = ref(null);
const theText = ref("");
const files = ref([]);
const previews = ref({});
const theSavedFiles = ref({});
const theInfoSwitch = ref(false);

const videoSource = ref("upload");
const youtubeUrl = ref("");

const isVideo = (file) => file.type.startsWith("video/");

onMounted(() => {
  token.value = localStorage.getItem("authToken");
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
  files.value = [];
  previews.value = {};
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

async function getAllData() {
  if (!dateStr.value) return alert("Velg en dag først");

  const response = await fetch(`${API_BASE_URL}/calendar/${dateStr.value}`, {
    headers: {
      Authorization: `Bearer ${token.value}`,
    },
  });

  if (response.status === 401) {
    alert("Logg inn på nytt");
    return router.push("/admin");
  }

  theSavedFiles.value = await response.json();
}

async function deleteData() {
  if (!theSavedFiles.value?.id) return alert("Ingen entry å slette");

  const response = await fetch(`http://127.0.0.1:5000/calendar/${theSavedFiles.value.id}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token.value}`,
    },
  });

  if (!response.ok) {
    alert("Sletting feilet");
    return;
  }

  alert("Slettet!");
  theSavedFiles.value = {};
  theInfoSwitch.value = false;
}


async function save() {
  if (!dateStr.value) return alert("Velg en dag først");
  if (!theText.value.trim()) return alert("Skriv inn tekst");

  if (videoSource.value === "upload" && files.value.length === 0) {
    return alert("Last opp en video eller velg YouTube");
  }
  if (videoSource.value === "youtube" && !youtubeUrl.value.trim()) {
    return alert("Skriv inn YouTube-lenke");
  }

  const formData = new FormData();
  formData.append("date", dateStr.value);
  formData.append("task_text", theText.value);
  formData.append("video_type", videoSource.value);
  formData.append("is_published", "true");

  if (videoSource.value === "upload") {
    files.value.forEach((file) => formData.append("files", file));
  } else {
    formData.append("youtube_url", youtubeUrl.value);
  }

  const response = await fetch(`${API_BASE_URL}/calendar`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token.value}`,
    },
    body: formData,
  });

  if (response.status === 401) {
    alert("Token utløpt, logg inn igjen");
    return router.push("/login");
  }

  if (!response.ok) {
    console.error(await response.text());
    return alert("Upload feilet.");
  }

  alert("Lagret!");

  selectedDay.value = null;
  theText.value = "";
  files.value = [];
  previews.value = {};
  youtubeUrl.value = "";
  videoSource.value = "upload";
}

function getYoutubeUrl() {
  if (!theSavedFiles.value?.video_path) return "";
  const url = theSavedFiles.value.video_path;
  const match = url.match(/(?:v=|\/embed\/|\/shorts\/|youtu\.be\/|\/v\/)([^?&\/\s]{11})/i);
  if (match && match[1]) {
    return `https://www.youtube.com/embed/${match[1]}`;
  }
  if (url.includes("/embed/")) {
    return url;
  }
  return "";
}

function isSavedVideo(path) {
  if (!path) return false;
  const ext = path.split(".").pop().toLowerCase();
  return ["mp4", "webm", "ogg"].includes(ext);
}

function getUploadUrl(path) {
  const filename = path.split(/[/\\]/).pop();
  return `${API_BASE_URL}/uploads/${encodeURIComponent(filename)}`;
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
        <option :value="null" disabled>– Velg dag –</option>
        <option v-for="day in 24" :key="day" :value="day">{{ day }}. desember</option>
      </select>

      <div class="mt-4">
        <label class="block mb-2 text-sm font-medium text-gray-700">
          Tekst for luke {{ selectedDay || "" }}:
        </label>
        <textarea
            v-model="theText"
            class="w-full h-full p-3 border border-gray-300 rounded-md min-h-[120px]"
            placeholder="Skriv tekst..."
            required
        ></textarea>
      </div>

      <div class="mt-8">
        <label class="block mb-4 text-lg font-medium text-gray-800">Hvor skal videoen komme fra?</label>
        <div class="flex gap-8">
          <label class="flex items-center">
            <input type="radio" v-model="videoSource" value="upload" class="mr-2" />
            Last opp egen video
          </label>
          <label class="flex items-center">
            <input type="radio" v-model="videoSource" value="youtube" class="mr-2" />
            YouTube-lenke
          </label>
        </div>
      </div>
    </div>

    <div class="bg-gray-100 rounded-lg shadow-lg p-6">
      <div v-if="videoSource === 'upload'">
        <label class="block mb-2 text-sm font-medium text-gray-700">Last opp video</label>
        <input
            class="w-full p-2 border border-gray-300 rounded-md mb-4"
            type="file"
            @change="onFileChange"
            accept="video/*"
        />

        <div
            v-for="file in files"
            :key="file.name"
            class="border border-gray-200 rounded-md p-3 bg-gray-50 mb-4"
        >
          <p class="text-sm text-gray-600 mb-2">
            {{ file.name }} ({{ formatBytes(file.size) }})
          </p>
          <video v-if="isVideo(file)" :src="previews[file.name]" controls class="h-32 rounded w-full"></video>
        </div>
      </div>

      <div v-else>
        <label class="block mb-2 text-sm font-medium text-gray-700">YouTube-lenke</label>
        <input
            v-model="youtubeUrl"
            type="url"
            placeholder="https://youtube.com/shorts/lRORFxM2P10?si=xk5leEDteJeGxT_q"
            class="w-full p-3 border border-gray-300 rounded-md"
        />
      </div>

      <button @click="save" class="mt-6 w-full bg-blue-900 text-white py-3 rounded-md hover:bg-blue-700 transition">
        Lagre luke {{ selectedDay || "" }}
      </button>

      <button
          @click="getAllData(); theInfoSwitch = !theInfoSwitch"
          class="mt-3 w-full bg-green-900 text-white py-3 rounded-md hover:bg-green-700 transition"
      >
        Hent info om denne luka
      </button>

      <div v-if="theInfoSwitch">
        <button
            @click="deleteData"
            class="mt-3 w-full bg-red-800 text-white py-3 rounded-md hover:bg-red-700 transition"
        >slett innhold</button>

        <pre class="mt-4 text-xl text-gray-600 bg-gray-800 text-white p-4 rounded overflow-auto font-medium">
          Dato: {{ theSavedFiles.date }}
        </pre>
        <pre class="mt-4 text-xl text-gray-600 bg-gray-800 text-white p-4 rounded overflow-auto font-medium">
          Luketekst: {{ theSavedFiles.task_text }}
        </pre>
        <pre class="mt-4 text-xl text-gray-600 bg-gray-800 text-white p-4 rounded overflow-auto font-medium">
          Videofil: {{ theSavedFiles.video_type }}
          <p v-if="theSavedFiles.video_type === 'youtube'">
            Videolink: {{theSavedFiles.video_path}}
          </p>
        </pre>
      </div>

      <div v-if="theInfoSwitch">
        <div v-if="theSavedFiles.video_type === 'youtube' && theSavedFiles.video_path">
          <iframe
              :src="getYoutubeUrl()"
              width="100%"
              height="315"
              frameborder="0"
              allowfullscreen
          ></iframe>
        </div>

        <div v-else-if="theSavedFiles.video_type === 'upload' && theSavedFiles.video_path" class="w-full mt-4">
          <template v-if="isSavedVideo(theSavedFiles.video_path)">
            <video width="100%" controls>
              <source :src="getUploadUrl(theSavedFiles.video_path)" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </template>
          <template v-else>
            <img
                :src="getUploadUrl(theSavedFiles.video_path)"
                alt="Uploaded content"
                class="w-full object-contain"
            />
          </template>
        </div>
      </div>

    </div>
  </div>
  <change-password></change-password>
</template>

