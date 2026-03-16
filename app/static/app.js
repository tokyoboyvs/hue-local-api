const apiKeyInput = document.getElementById("api-key");
const lightSelect = document.getElementById("light-select");
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

const loadLights = async () => {
  clearFeedback();

  try {
    const response = await fetch("/api/lights", {
      headers: getHeaders(),
    });

    const data = await response.json();

    if (!response.ok) {
      setFeedback(data.detail || "Unable to load lights");
      lightSelect.innerHTML = '<option value="">No lights available</option>';
      return;
    }

    lightSelect.innerHTML = '<option value="">Select a light</option>';

    for (const light of data.items) {
      const option = document.createElement("option");
      option.value = light.id;
      option.textContent = `${light.name} (${light.room})`;
      lightSelect.appendChild(option);
    }
  } catch {
    setFeedback("Unable to reach API");
  }
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

apiKeyInput.addEventListener("input", loadLights);
loadLightButton.addEventListener("click", loadSelectedLight);
turnOnButton.addEventListener("click", () => runLightAction("on"));
turnOffButton.addEventListener("click", () => runLightAction("off"));
toggleButton.addEventListener("click", () => runLightAction("toggle"));

brightnessRange.addEventListener("input", () => {
  brightnessValue.textContent = `${brightnessRange.value}%`;
});

applyBrightnessButton.addEventListener("click", updateBrightness);
applyColorButton.addEventListener("click", updateColor);

loadLights();
