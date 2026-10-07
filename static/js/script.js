const $ = (selector) => document.querySelector(selector);
const checklistLabels = { length: "At least 12 characters", uppercase: "Contains uppercase letters", lowercase: "Contains lowercase letters", numbers: "Contains numbers", symbols: "Contains special characters", not_common: "Does not contain common passwords", no_sequences: "Does not contain obvious sequences", no_excessive_repetition: "Does not contain excessive repeated characters" };

function renderAnalysis(data) {
  $("#strength").textContent = data.strength;
  $("#score").textContent = `${data.score}/100`;
  $("#entropy").textContent = `${data.entropy} bits`;
  const bar = $("#score-bar"); bar.style.width = `${data.score}%`;
  bar.style.background = data.score < 45 ? "var(--danger)" : data.score < 70 ? "#f0c85b" : "var(--green)";
  $("#checklist").innerHTML = Object.entries(data.checks).map(([key, value]) => `<li class="${value ? "ok" : ""}">${value ? "✓" : "✕"} ${checklistLabels[key]}</li>`).join("");
  $("#recommendations").innerHTML = data.recommendations.map((item) => `<li>${item}</li>`).join("");
}

$("#analyze-button").addEventListener("click", async () => {
  const response = await fetch("/api/analyze", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ password: $("#password").value }) });
  const data = await response.json();
  if (!response.ok) { window.alert(data.error || "Unable to analyze password."); return; }
  renderAnalysis(data);
});
$("#toggle-password").addEventListener("click", () => { const field = $("#password"); field.type = field.type === "password" ? "text" : "password"; });
$("#clear-password").addEventListener("click", () => { $("#password").value = ""; $("#password").focus(); });
$("#length").addEventListener("input", (event) => { $("#length-value").textContent = event.target.value; });
$("#generate-button").addEventListener("click", async () => {
  const params = new URLSearchParams({ length: $("#length").value });
  document.querySelectorAll("[data-option]").forEach((input) => params.set(input.dataset.option, input.checked));
  const response = await fetch(`/api/generate?${params}`);
  const data = await response.json();
  if (!response.ok) { window.alert(data.error || "Unable to generate password."); return; }
  $("#generated-password").textContent = data.password;
});
$("#copy-button").addEventListener("click", async () => {
  const value = $("#generated-password").textContent;
  if (!value || value.startsWith("Click generate")) return;
  await navigator.clipboard.writeText(value);
  $("#copy-button").textContent = "Copied";
  setTimeout(() => { $("#copy-button").textContent = "Copy"; }, 1200);
});
