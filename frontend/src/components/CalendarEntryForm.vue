<script setup>
import { ref, computed, onUnmounted, watch } from 'vue';

// Props: Tar inn data hvis man skal redigere en eksisterende luke
const props = defineProps({
    entryToEdit: {
        type: Object,
        default: null
    }
});

const emit = defineEmits(['saved', 'cancel']);

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Lokale variabler
const selectedDay = ref(null);
const textContent = ref("");
const videoSource = ref("upload"); // 'upload' eller 'youtube'
const youtubeUrl = ref("");
const files = ref([]);
const previews = ref({});
const isLoading = ref(false);

const isEditMode = computed(() => props.entryToEdit !== null);

// Hvis vi er i redigeringsmodus, fyll inn feltene med eksisterende data
watch(() => props.entryToEdit, (newVal) => {
    if (newVal) {
        // Henter ut dagen (siste del av "2025-12-01") og gjør om til tall
        selectedDay.value = parseInt(newVal.date.split("-").pop());
        textContent.value = newVal.task_text || "";
        if (newVal.video_type === 'youtube') {
            videoSource.value = 'youtube';
            youtubeUrl.value = newVal.video_url || newVal.youtube_url || ""; // Sjekker begge felter for sikkerhets skyld
        } else if (newVal.video_type === 'upload') {
            videoSource.value = 'upload';
            // Merk: Vi kan ikke forhåndsvise opplastede filer uten å laste dem inn på nytt
        }
    } else {
        resetForm();
    }
}, { immediate: true });

const dateStr = computed(() => {
    if (!selectedDay.value) return null;
    return `2025-12-${String(selectedDay.value).padStart(2, "0")}`;
});

const isVideo = (file) => file.type.startsWith("video/");

function formatBytes(bytes) {
    const units = ["Bytes", "KB", "MB", "GB"];
    if (!bytes) return "0 Bytes";
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return (bytes / Math.pow(1024, i)).toFixed(2) + " " + units[i];
}

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

function resetForm() {
    selectedDay.value = null;
    textContent.value = "";
    files.value = [];
    previews.value = {};
    youtubeUrl.value = "";
    videoSource.value = "upload";
}

async function save() {
    if (!dateStr.value) return alert("Velg en dag først");
    if (!textContent.value.trim()) return alert("Skriv inn tekst");

    // Validering kun for NY oppretting eller hvis vi bytter kilde
    if (!isEditMode.value) {
        if (videoSource.value === "upload" && files.value.length === 0) {
            return alert("Last opp en video eller velg YouTube");
        }
        if (videoSource.value === "youtube" && !youtubeUrl.value.trim()) {
            return alert("Skriv inn YouTube-lenke");
        }
    }

    const token = localStorage.getItem("authToken");
    if (!token) return alert("Du må være logget inn");

    isLoading.value = true;

    try {
        let url = `${API_BASE_URL}/calendar`;
        let method = "POST";
        let body;
        let headers = { Authorization: `Bearer ${token}` };

        if (isEditMode.value) {
            // --- REDIGERING (PUT) ---
            url = `${API_BASE_URL}/calendar/${props.entryToEdit.id}`;
            method = "PUT";

            // Backend forventer JSON ved PUT i følge koden din
            headers["Content-Type"] = "application/json";

            const payload = {
                date: dateStr.value, // Backend ser ut til å ignorere dato ved update, men vi sender med
                task_text: textContent.value,
                is_published: true
            };

            // Backend støtter foreløpig bare tekst/publisert endring via JSON PUT.
            // Hvis du vil oppdatere video via PUT må backend endres til å ta imot fil/formdata også der, 
            // eller du må lage en egen logikk. For nå sender vi video-URL hvis det er youtube.
            if (videoSource.value === "youtube") {
                payload.youtube_url = youtubeUrl.value;
            }

            body = JSON.stringify(payload);

        } else {
            // --- NY OPPFØRING (POST) ---
            const formData = new FormData();
            formData.append("date", dateStr.value);
            formData.append("task_text", textContent.value);
            formData.append("video_type", videoSource.value);
            formData.append("is_published", "true");

            if (videoSource.value === "upload") {
                files.value.forEach((file) => formData.append("files", file));
            } else {
                formData.append("youtube_url", youtubeUrl.value);
            }
            body = formData; // Fetch setter Content-Type automatisk for FormData
        }

        const response = await fetch(url, { method, headers, body });

        if (!response.ok) {
            const errText = await response.text();
            console.error(errText);
            throw new Error("Lagring feilet: " + errText);
        }

        alert(isEditMode.value ? "Endringer lagret!" : "Luke opprettet!");
        resetForm();
        emit("saved"); // Gi beskjed til forelder at vi er ferdige

    } catch (error) {
        alert(error.message);
    } finally {
        isLoading.value = false;
    }
}
</script>

<template>
    <div class="bg-gray-100 rounded-lg shadow-lg p-10">
        <h2 class="text-xl font-bold mb-4">
            {{ isEditMode ? 'Rediger Luke' : 'Opprett Ny Luke' }}
            <span v-if="isEditMode" class="text-sm font-normal text-gray-500 ml-2">(ID: {{ entryToEdit.id }})</span>
        </h2>

        <label class="block mb-2 text-sm font-medium text-gray-700">Velg dag</label>
        <select v-model="selectedDay" class="w-full p-3 border border-gray-300 rounded-md" required>
            <option :value="null" disabled>– Velg dag –</option>
            <option v-for="day in 24" :key="day" :value="day">{{ day }}. desember</option>
        </select>

        <div class="mt-4">
            <label class="block mb-2 text-sm font-medium text-gray-700">
                Tekst for luke {{ selectedDay || "" }}:
            </label>
            <textarea v-model="textContent" class="w-full h-full p-3 border border-gray-300 rounded-md min-h-[120px]"
                placeholder="Skriv tekst..." required></textarea>
        </div>

        <!-- Video valg -->
        <div class="mt-8">
            <label class="block mb-4 text-lg font-medium text-gray-800">Hvor skal videoen komme fra?</label>
            <div class="flex gap-8">
                <label class="flex items-center">
                    <input type="radio" v-model="videoSource" value="upload" class="mr-2" :disabled="isEditMode" />
                    Last opp egen video <span v-if="isEditMode" class="text-xs text-red-500 ml-1">(Kun ved ny)</span>
                </label>
                <label class="flex items-center">
                    <input type="radio" v-model="videoSource" value="youtube" class="mr-2" />
                    YouTube-lenke
                </label>
            </div>
        </div>

        <!-- Video input felter -->
        <div class="mt-4 p-4 bg-white rounded border border-gray-200">
            <div v-if="videoSource === 'upload'">
                <p v-if="isEditMode" class="text-sm text-gray-500 italic mb-2">
                    Merk: Oppdatering av fil er ikke støttet i redigering ennå (backend begrensning).
                </p>
                <div v-else>
                    <input class="w-full p-2 border border-gray-300 rounded-md mb-4" type="file" @change="onFileChange"
                        accept="video/*" />
                    <div v-for="file in files" :key="file.name"
                        class="border border-gray-200 rounded-md p-3 bg-gray-50 mb-4">
                        <p class="text-sm text-gray-600 mb-2">{{ file.name }} ({{ formatBytes(file.size) }})</p>
                        <video v-if="isVideo(file)" :src="previews[file.name]" controls
                            class="h-32 rounded w-full"></video>
                    </div>
                </div>
            </div>

            <div v-else>
                <input v-model="youtubeUrl" type="url" placeholder="https://youtube.com/..."
                    class="w-full p-3 border border-gray-300 rounded-md" />
            </div>
        </div>

        <div class="flex gap-4 mt-6">
            <button @click="save" :disabled="isLoading"
                class="flex-1 bg-blue-900 text-white py-3 rounded-md hover:bg-blue-700 transition">
                {{ isLoading ? 'Lagrer...' : (isEditMode ? 'Oppdater Luke' : 'Lagre Ny Luke') }}
            </button>
            <button v-if="isEditMode" @click="$emit('cancel')"
                class="px-6 bg-gray-300 text-gray-800 rounded-md hover:bg-gray-400">
                Avbryt
            </button>
        </div>
    </div>
</template>