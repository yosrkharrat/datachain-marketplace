const API_BASE = "http://localhost:8000";

const form = document.getElementById("analyze-form");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const submitBtn = document.getElementById("submit-btn");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const file = formData.get("file");

  if (!file || file.size === 0) {
    setStatus("Please choose a dataset file.", true);
    return;
  }

  submitBtn.disabled = true;
  setStatus("Analyzing dataset...", false);

  try {
    const response = await fetch(`${API_BASE}/api/analyze`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Analysis failed");
    }

    renderReport(data);
    setStatus("Analysis complete. Ready for registry flow.", false);
  } catch (error) {
    setStatus(error.message || "Request failed", true);
  } finally {
    submitBtn.disabled = false;
  }
});

function renderReport(payload) {
  const analysis = payload.raw_analysis || {};

  document.getElementById("rows").textContent = analysis.rows ?? "-";
  document.getElementById("columns").textContent = analysis.columns ?? "-";
  document.getElementById("missing").textContent = analysis.missing_percentage ?? "-";
  document.getElementById("quality").textContent = analysis.quality_score ?? "-";

  const tagsEl = document.getElementById("tags");
  tagsEl.innerHTML = "";
  (analysis.tags || []).forEach((tag) => {
    const chip = document.createElement("b");
    chip.textContent = tag;
    tagsEl.appendChild(chip);
  });

  document.getElementById("description").textContent =
    payload.metadata?.semantic_description || "No description generated.";

  const useCasesEl = document.getElementById("use-cases");
  useCasesEl.innerHTML = "";
  (payload.metadata?.suggested_use_cases || []).forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.use_case} (${item.confidence}) - ${item.reason}`;
    useCasesEl.appendChild(li);
  });

  resultEl.classList.remove("hidden");
}

function setStatus(message, isError) {
  statusEl.textContent = message;
  statusEl.style.color = isError ? "#b72f2f" : "#125b50";
}
