/* script.js
   Frontend logic:
   - loads events from backend
   - adds event (POST)
   - deletes event (DELETE)
   - shows live countdown per event
*/

const API_BASE = "http://127.0.0.1:8000/api/events/"; // Django backend API base

// DOM elements
const addBtn = document.getElementById("addBtn");
const evName = document.getElementById("evName");
const evDate = document.getElementById("evDate");
const evDesc = document.getElementById("evDesc");
const eventsList = document.getElementById("eventsList");

// store intervals to clear later
const intervals = {};

// fetch and render events
async function loadEvents() {
  try {
    const res = await fetch(API_BASE);
    if (!res.ok) throw new Error("Failed to fetch");
    const events = await res.json();
    renderEvents(events);
  } catch (err) {
    console.error(err);
    eventsList.innerHTML = "<p style='grid-column:1/-1;color:#d00'>Unable to load events.</p>";
  }
}

function renderEvents(events) {
  eventsList.innerHTML = "";
  // clear previous intervals
  for (let k in intervals) {
    clearInterval(intervals[k]);
  }

  events.forEach(ev => {
    const card = document.createElement("div");
    card.className = "event-card";
    card.innerHTML = `
      <h3>${escapeHtml(ev.name)}</h3>
      <p>${escapeHtml(ev.description || "")}</p>
      <div>Target: ${new Date(ev.date).toLocaleString()}</div>
      <div class="timer" id="timer-${ev.id}">--</div>
      <div class="actions">
        <button class="action-btn delete" data-id="${ev.id}">Delete</button>
      </div>
    `;
    eventsList.appendChild(card);

    // attach delete handler
    card.querySelector(".delete").addEventListener("click", () => deleteEvent(ev.id));

    // start countdown interval
    startTimer(ev.id, ev.date);
  });
}

// helper to sanitize
function escapeHtml(s) {
  if (!s) return "";
  return String(s).replace(/[&<>"'\/]/g, function (c) {
    return ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;',
      '/': '&#x2F;'
    })[c];
  });
}

// start countdown for a given target date, update DOM every second
function startTimer(id, dateStr) {
  const el = document.getElementById(`timer-${id}`);
  if (!el) return;
  function update() {
    const now = new Date();
    const target = new Date(dateStr);
    const diff = target - now;
    if (diff <= 0) {
      el.textContent = "✅ Event started";
      clearInterval(intervals[id]);
      return;
    }
    const d = Math.floor(diff / (1000 * 60 * 60 * 24));
    const h = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const m = Math.floor((diff / (1000 * 60)) % 60);
    const s = Math.floor((diff / 1000) % 60);
    el.textContent = `${d}d ${pad(h)}h ${pad(m)}m ${pad(s)}s`;
  }
  update();
  intervals[id] = setInterval(update, 1000);
}

function pad(n) { return n.toString().padStart(2, '0'); }

// Add event - POST
async function addEvent() {
  const name = evName.value.trim();
  const date = evDate.value;
  const desc = evDesc.value.trim();
  if (!name || !date) {
    alert("Please enter event name and date/time.");
    return;
  }

  try {
    const res = await fetch(API_BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, date, description: desc })
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(err || "Failed to create event");
    }
    evName.value = ""; evDate.value = ""; evDesc.value = "";
    loadEvents();
  } catch (err) {
    console.error(err);
    alert("Error adding event");
  }
}

// Delete event - DELETE
async function deleteEvent(id) {
  if (!confirm("Delete this event?")) return;
  try {
    const res = await fetch(API_BASE + id + "/", { method: "DELETE" });
    if (!res.ok) throw new Error("Delete failed");
    loadEvents();
  } catch (err) {
    console.error(err);
    alert("Error deleting event");
  }
}

addBtn.addEventListener("click", addEvent);

// initial load
loadEvents();
// FAQ Accordion Script
document.querySelectorAll(".faq-question").forEach(button => {
  button.addEventListener("click", () => {
    const faqItem = button.parentElement;

    // Close all other FAQs
    document.querySelectorAll(".faq-item").forEach(item => {
      if (item !== faqItem) item.classList.remove("active");
    });

    // Toggle the clicked FAQ
    faqItem.classList.toggle("active");
  });
});
