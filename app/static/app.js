const API_KEY_STORAGE_KEY = "hue-local-api-key";

const apiKeyInput = document.getElementById("api-key");
const lightSelect = document.getElementById("light-select");
const roomSelect = document.getElementById("room-select");
const loadLightButton = document.getElementById("load-light-btn");
const statusCard = document.getElementById("status-card");
const feedback = document.getElementById("feedback");

const lightId = document.getElementById("light-id");
const lightName = document.getElementById("light-name");
const lightRoom = document.getElementById("light-room");
const lightPower = document.getElementById("light-power");
const lightBrightness = document.getElementById("light-brightness");
const lightColor = document.getElementById("light-color");

const turnOnButton = document.getElementById("turn-on-btn");
const turnOffButton = document.getElementById("turn-off-btn");
const toggleButton = document.getElementById("toggle-btn");

const bulkLightSelect = document.getElementById("bulk-light-select");
const bulkOnButton = document.getElementById("bulk-on-btn");
const bulkOffButton = document.getElementById("bulk-off-btn");
const bulkToggleButton = document.getElementById("bulk-toggle-btn");

const brightnessRange = document.getElementById("brightness-range");
const brightnessValue = document.getElementById("brightness-value");
const applyBrightnessButton = document.getElementById("apply-brightness-btn");
const colorPicker = document.getElementById("color-picker");
const applyColorButton = document.getElementById("apply-color-btn");

const getHeaders = () => {
  return {
    accept: "application/json",
    "X-API-Key": apiKeyInput.value,
  };
};

const setFeedback = (message) => {
  feedback.textContent = message;
};

const clearFeedback = () => {
  feedback.textContent = "";
};

const saveApiKey = () => {
  try {
    localStorage.setItem(API_KEY_STORAGE_KEY, apiKeyInput.value.trim());
  } catch {
    setFeedback("Unable to save API key in browser storage");
  }
};

const loadSavedApiKey = () => {
  try {
    const savedApiKey = localStorage.getItem(API_KEY_STORAGE_KEY);

    if (savedApiKey !== null) {
      apiKeyInput.value = savedApiKey;
    }
  } catch {
    setFeedback("Unable to read API key from browser storage");
  }
};

const renderLight = (light) => {
  lightId.textContent = light.id;
  lightName.textContent = light.name;
  lightRoom.textContent = light.room;
  lightPower.textContent = light.is_on ? "on" : "off";
  lightBrightness.textContent = `${light.brightness}%`;
  lightColor.textContent = light.color;

  brightnessRange.value = light.brightness;
  brightnessValue.textContent = `${light.brightness}%`;
  colorPicker.value = light.color;

  statusCard.classList.remove("hidden");
};

const getSelectedLightId = () => {
  return lightSelect.value;
};

const getSelectedLightIds = () => {
  return Array.from(bulkLightSelect.selectedOptions).map((option) => option.value);
};

const loadLights = async () => {
  clearFeedback();

  const selectedRoom = roomSelect.value;
  const endpoint = selectedRoom ? `/api/rooms/${selectedRoom}/lights` : "/api/lights";

  try {
    const response = await fetch(endpoint, {
      headers: getHeaders(),
    });

    const data = await response.json();

    if (!response.ok) {
      setFeedback(data.detail || "Unable to load lights");
      lightSelect.innerHTML = '<option value="">No lights available</option>';
      return;
    }

    lightSelect.innerHTML = '<option value="">Select a light</option>';
    bulkLightSelect.innerHTML = "";

    for (const light of data.items) {
      const option = document.createElement("option");
      option.value = light.id;
      option.textContent = `${light.name} (${light.room})`;
      lightSelect.appendChild(option);

      const bulkOption = document.createElement("option");
      bulkOption.value = light.id;
      bulkOption.textContent = `${light.name} (${light.room})`;
      bulkLightSelect.appendChild(bulkOption);
    }
  } catch {
    setFeedback("Unable to reach API");
  }
};

const loadRooms = async () => {
  try {
    const response = await fetch("/api/rooms", {
      headers: getHeaders(),
    });

    const data = await response.json();

    if (!response.ok) {
      roomSelect.innerHTML = '<option value="">All rooms</option>';
      return;
    }

    roomSelect.innerHTML = '<option value="">All rooms</option>';

    for (const room of data.items) {
      const option = document.createElement("option");
      option.value = room.name;
      option.textContent = `${room.name} (${room.light_count})`;
      roomSelect.appendChild(option);
    }
  } catch {
    roomSelect.innerHTML = '<option value="">All rooms</option>';
  }
};

const loadRoomsAndLights = async () => {
  await loadRooms();
  await loadLights();
};

const loadSelectedLight = async () => {
  clearFeedback();

  const selectedLightId = lightSelect.value;

  if (!selectedLightId) {
    setFeedback("Select a light first");
    return;
  }

  try {
    const response = await fetch(`/api/lights/${selectedLightId}`, {
      headers: getHeaders(),
    });

    const data = await response.json();

    if (!response.ok) {
      setFeedback(data.detail || "Unable to load light");
      return;
    }

    renderLight(data.item);
  } catch {
    setFeedback("Unable to reach API");
  }
};

const runLightAction = async (action) => {
  clearFeedback();

  const selectedLightId = getSelectedLightId();

  if (!selectedLightId) {
    setFeedback("Select a light first");
    return;
  }

  try {
    const response = await fetch(`/api/lights/${selectedLightId}/${action}`, {
      method: "POST",
      headers: getHeaders(),
    });

    const data = await response.json();

    if (!response.ok) {
      setFeedback(data.detail || `Unable to ${action} light`);
      return;
    }

    renderLight(data.light);
  } catch {
    setFeedback("Unable to reach API");
  }
};

const updateBrightness = async () => {
  clearFeedback();

  const selectedLightId = getSelectedLightId();

  if (!selectedLightId) {
    setFeedback("Select a light first");
    return;
  }

  try {
    const response = await fetch(`/api/lights/${selectedLightId}/brightness`, {
      method: "POST",
      headers: {
        ...getHeaders(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        brightness: Number(brightnessRange.value),
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      setFeedback(data.detail || "Unable to update light brightness");
      return;
    }

    renderLight(data.light);
  } catch {
    setFeedback("Unable to reach API");
  }
};

const updateColor = async () => {
  clearFeedback();

  const selectedLightId = getSelectedLightId();

  if (!selectedLightId) {
    setFeedback("Select a light first");
    return;
  }

  try {
    const response = await fetch(`/api/lights/${selectedLightId}/color`, {
      method: "POST",
      headers: {
        ...getHeaders(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        color: colorPicker.value,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      setFeedback(data.detail || "Unable to update color");
      return;
    }

    renderLight(data.light);
  } catch {
    setFeedback("Unable to reach API");
  }
};

const runBulkLightAction = async (action) => {
  clearFeedback();

  const selectedLightIds = getSelectedLightIds();

  if (selectedLightIds.length === 0) {
    setFeedback("Select at least one light");
    return;
  }

  try {
    const response = await fetch(`/api/lights/actions/${action}`, {
      method: "POST",
      headers: {
        ...getHeaders(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        light_ids: selectedLightIds,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      setFeedback(data.detail || `Unable to execute bulk ${action}`);
      return;
    }

    if (data.missing_light_ids.length > 0) {
      setFeedback(`Missing lights: ${data.missing_light_ids.join(", ")}`);
    }

    await loadLights();
  } catch {
    setFeedback("Unable to reach API");
  }
};

apiKeyInput.addEventListener("input", () => {
  saveApiKey();
  loadRoomsAndLights();
});

apiKeyInput.addEventListener("change", saveApiKey);
apiKeyInput.addEventListener("blur", saveApiKey);

roomSelect.addEventListener("change", loadLights);
loadLightButton.addEventListener("click", loadSelectedLight);

turnOnButton.addEventListener("click", () => runLightAction("on"));
turnOffButton.addEventListener("click", () => runLightAction("off"));
toggleButton.addEventListener("click", () => runLightAction("toggle"));

bulkOnButton.addEventListener("click", () => runBulkLightAction("on"));
bulkOffButton.addEventListener("click", () => runBulkLightAction("off"));
bulkToggleButton.addEventListener("click", () => runBulkLightAction("toggle"));

brightnessRange.addEventListener("input", () => {
  brightnessValue.textContent = `${brightnessRange.value}%`;
});

applyBrightnessButton.addEventListener("click", updateBrightness);
applyColorButton.addEventListener("click", updateColor);

loadSavedApiKey();
loadRoomsAndLights();
