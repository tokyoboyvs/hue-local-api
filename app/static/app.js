const API_KEY_STORAGE_KEY = "hue-local-api-key";

const apiKeyInput = document.getElementById("api-key");
const lightSelect = document.getElementById("light-select");
const roomSelect = document.getElementById("room-select");
const resetRoomFilterButton = document.getElementById("reset-room-filter-btn");
const loadLightButton = document.getElementById("load-light-btn");
const refreshUiButton = document.getElementById("refresh-ui-btn");
const statusCard = document.getElementById("status-card");
const feedback = document.getElementById("feedback");

const lightId = document.getElementById("light-id");
const lightName = document.getElementById("light-name");
const lightRoom = document.getElementById("light-room");
const lightPower = document.getElementById("light-power");
const lightBrightness = document.getElementById("light-brightness");
const lightColorPreview = document.getElementById("light-color-preview");
const lightColor = document.getElementById("light-color");

const turnOnButton = document.getElementById("turn-on-btn");
const turnOffButton = document.getElementById("turn-off-btn");
const toggleButton = document.getElementById("toggle-btn");

const selectAllBulkButton = document.getElementById("select-all-bulk-btn");
const clearBulkButton = document.getElementById("clear-bulk-btn");

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

const setFeedback = (message, type = "neutral") => {
  feedback.textContent = message;
  feedback.className = `feedback feedback-${type}`;
};

const clearFeedback = () => {
  feedback.textContent = "";
  feedback.className = "feedback feedback-neutral";
};

const saveApiKey = () => {
  try {
    localStorage.setItem(API_KEY_STORAGE_KEY, apiKeyInput.value.trim());
  } catch {
    setFeedback("Unable to save API key in browser storage", "error");
  }
};

const loadSavedApiKey = () => {
  try {
    const savedApiKey = localStorage.getItem(API_KEY_STORAGE_KEY);

    if (savedApiKey !== null) {
      apiKeyInput.value = savedApiKey;
    }
  } catch {
    setFeedback("Unable to read API key from browser storage", "error");
  }
};

const renderLight = (light) => {
  lightId.textContent = light.id;
  lightName.textContent = light.name;
  lightRoom.textContent = light.room;
  lightPower.textContent = light.is_on ? "on" : "off";
  lightPower.className = light.is_on ? "power-badge power-on" : "power-badge power-off";
  lightBrightness.textContent = `${light.brightness}%`;
  lightColor.textContent = light.color;
  lightColorPreview.style.backgroundColor = light.color;

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

const selectAllBulkLights = () => {
  for (const option of bulkLightSelect.options) {
    option.selected = true;
  }

  setFeedback("All visible lights selected", "success");
};

const clearBulkSelection = () => {
  for (const option of bulkLightSelect.options) {
    option.selected = false;
  }

  setFeedback("Bulk selection cleared", "neutral");
};

const resetRoomFilter = async () => {
  roomSelect.value = "";
  await loadLights();

  if (!lightSelect.value) {
    await loadSelectedLight();
  } else {
    hideLightDetails();
    setFeedback("Room filter cleared", "neutral");
  }
};

const hideLightDetails = () => {
  statusCard.classList.add("hidden");
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
      setFeedback(data.detail || "Unable to load lights", "error");
      lightSelect.innerHTML = '<option value="">No lights available</option>';
      bulkLightSelect.innerHTML = "";
      hideLightDetails();
      return;
    }

    lightSelect.innerHTML = '<option value="">Select a light</option>';
    bulkLightSelect.innerHTML = "";

    const currentSelectedLightId = lightId.textContent;
    let selectedLightStillVisible = false;

    for (const light of data.items) {
      const option = document.createElement("option");
      option.value = light.id;
      option.textContent = `${light.name} (${light.room})`;
      lightSelect.appendChild(option);

      const bulkOption = document.createElement("option");
      bulkOption.value = light.id;
      bulkOption.textContent = `${light.name} (${light.room})`;
      bulkLightSelect.appendChild(bulkOption);

      if (light.id === currentSelectedLightId) {
        selectedLightStillVisible = true;
      }
    }

    if (data.items.length > 0 && !lightSelect.value) {
      lightSelect.value = data.items[0].id;
    }

    if (data.items.length > 0) {
      setFeedback(`${data.items.length} light(s) loaded`, "success");
    } else {
      setFeedback("No lights available", "neutral");
    }

    if (currentSelectedLightId && !selectedLightStillVisible) {
      hideLightDetails();
    }
  } catch {
    setFeedback("Unable to reach API", "error");
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

  if (lightSelect.value) {
    await loadSelectedLight();
  }
};

const refreshUi = async () => {
  clearFeedback();

  const currentSelectedLightId = lightId.textContent;

  await loadRooms();
  await loadLights();

  if (currentSelectedLightId) {
    const optionExists = Array.from(lightSelect.options).some((option) => option.value === currentSelectedLightId);

    if (optionExists) {
      lightSelect.value = currentSelectedLightId;
      await loadSelectedLight();
      return;
    }
  }

  setFeedback("Interface refreshed", "success");
};

const loadSelectedLight = async () => {
  clearFeedback();

  const selectedLightId = lightSelect.value;

  if (!selectedLightId) {
    setFeedback("Select a light first", "error");
    return;
  }

  try {
    const response = await fetch(`/api/lights/${selectedLightId}`, {
      headers: getHeaders(),
    });

    const data = await response.json();

    if (!response.ok) {
      setFeedback(data.detail || "Unable to load light", "error");
      return;
    }

    renderLight(data.item);
    setFeedback(`Light '${data.item.name}' loaded`, "success");
  } catch {
    setFeedback("Unable to reach API", "error");
  }
};

const runLightAction = async (action) => {
  clearFeedback();

  const selectedLightId = getSelectedLightId();

  if (!selectedLightId) {
    setFeedback("Select a light first", "error");
    return;
  }

  try {
    const response = await fetch(`/api/lights/${selectedLightId}/${action}`, {
      method: "POST",
      headers: getHeaders(),
    });

    const data = await response.json();

    if (!response.ok) {
      setFeedback(data.detail || `Unable to ${action} light`, "error");
      return;
    }

    renderLight(data.light);
    setFeedback(data.message, "success");
  } catch {
    setFeedback("Unable to reach API", "error");
  }
};

const updateBrightness = async () => {
  clearFeedback();

  const selectedLightId = getSelectedLightId();

  if (!selectedLightId) {
    setFeedback("Select a light first", "error");
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
      setFeedback(data.detail || "Unable to update light brightness", "error");
      return;
    }

    renderLight(data.light);
    setFeedback(data.message, "success");
  } catch {
    setFeedback("Unable to reach API", "error");
  }
};

const updateColor = async () => {
  clearFeedback();

  const selectedLightId = getSelectedLightId();

  if (!selectedLightId) {
    setFeedback("Select a light first", "error");
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
      setFeedback(data.detail || "Unable to update color", "error");
      return;
    }

    renderLight(data.light);
    setFeedback(data.message, "success");
  } catch {
    setFeedback("Unable to reach API", "error");
  }
};

const runBulkLightAction = async (action) => {
  clearFeedback();

  const selectedLightIds = getSelectedLightIds();

  if (selectedLightIds.length === 0) {
    setFeedback("Select at least one light", "error");
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
      setFeedback(data.detail || `Unable to execute bulk ${action}`, "error");
      return;
    }

    if (data.missing_light_ids.length > 0) {
      setFeedback(`Missing lights: ${data.missing_light_ids.join(", ")}`, "error");
    } else {
      setFeedback(data.message, "success");
    }

    await loadLights();

    const selectedLightId = getSelectedLightId();

    if (selectedLightId) {
      await loadSelectedLight();
    }
  } catch {
    setFeedback("Unable to reach API", "error");
  }
};

apiKeyInput.addEventListener("input", () => {
  saveApiKey();
  loadRoomsAndLights();
});

apiKeyInput.addEventListener("change", saveApiKey);
apiKeyInput.addEventListener("blur", saveApiKey);

roomSelect.addEventListener("change", async () => {
  await loadLights();

  if (lightSelect.value) {
    await loadSelectedLight();
  }
});

resetRoomFilterButton.addEventListener("click", resetRoomFilter);

loadLightButton.addEventListener("click", loadSelectedLight);
refreshUiButton.addEventListener("click", refreshUi);

turnOnButton.addEventListener("click", () => runLightAction("on"));
turnOffButton.addEventListener("click", () => runLightAction("off"));
toggleButton.addEventListener("click", () => runLightAction("toggle"));

selectAllBulkButton.addEventListener("click", selectAllBulkLights);
clearBulkButton.addEventListener("click", clearBulkSelection);

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
