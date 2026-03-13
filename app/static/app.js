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
  statusCard.classList.remove("hidden");
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

apiKeyInput.addEventListener("change", loadLights);
loadLightButton.addEventListener("click", loadSelectedLight);

loadLights();
