<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import ChangePassword from "../components/ChangePassword.vue";
import CalendarEntryForm from "../components/CalendarEntryForm.vue";
import TheList from "../components/TheList.vue";
import Footer from '../components/Footer.vue'

const router = useRouter();
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";
const token = ref(null);

// State for redigering (sendes til form-komponenten)
const entryToEdit = ref(null);

// Referanse til liste-komponenten for å kunne laste på nytt etter lagring
const listRef = ref(null); 

onMounted(() => {
  token.value = localStorage.getItem("authToken");
  if (!token.value) router.push("/login");
});

// Kalles fra listen når man trykker "Rediger"
function handleEditRequest(entry) {
    entryToEdit.value = entry;
    // Scroll til toppen så man ser skjemaet
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Kalles fra skjemaet når lagring er ferdig
function onFormSaved() {
    entryToEdit.value = null; // Gå tilbake til "ny"-modus
    // Last listen på nytt for å vise endringene!
    if (listRef.value) {
        listRef.value.loadAll();
    }
}

// Slette-funksjon som sendes til listen
async function deleteData(entry) {
  if (!entry?.id) return;

  if(!confirm(`Er du sikker på at du vil slette luken for ${entry.date}?`)) return;

  const response = await fetch(`${API_BASE_URL}/calendar/${entry.id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token.value}` },
  });

  if (!response.ok) {
    alert("Sletting feilet");
    return;
  }

  // Oppdater listen automatisk etter sletting
  if (listRef.value) listRef.value.loadAll();
}
</script>

<template>
  <div class="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-8 p-6 bg-gray-50 min-h-screen">
    
    <div class="col-span-full">
      <h1 class="text-3xl font-bold text-gray-900 bg-blue-100 text-center py-4 rounded border border-blue-200">
        🎅 Admin - Julekalender
      </h1>
    </div>

    <!-- VENSTRE SIDE: SKJEMA -->
    <div class="lg:col-span-1">
        <div class="sticky top-6">
            <CalendarEntryForm 
                :entryToEdit="entryToEdit" 
                @saved="onFormSaved"
                @cancel="entryToEdit = null"
            />
            
            <!-- Passord-bytte under skjemaet -->
            <div class="bg-gray-100 rounded-lg shadow-lg p-10 mt-8">
                <ChangePassword />
            </div>
        </div>
    </div>

    <!-- HØYRE SIDE: LISTE (Erstatter den gamle "Sjekk innhold") -->
    <div class="lg:col-span-1">
        <!-- Vi bruker ref="listRef" for å kunne kalle loadAll() utenfra -->
        <TheList 
            ref="listRef"
            :onDelete="deleteData" 
            @edit="handleEditRequest" 
        />
    </div>
  </div>
  <Footer />
</template>