async function getRecommendation() {
  const btn = document.getElementById("submitBtn");
  const output = document.getElementById("output");
  const result = document.getElementById("resultCard");

  btn.disabled = true;
  btn.innerText = "Thinking...";
  result.classList.remove("hidden");
  output.innerText = "Analyzing your profile with AI…";

  const payload = {
    education_type: education_type.value,
    age_group: age_group.value,
    current_education: current_education.value,
    technical_skills: technical_skills.value,
    soft_skills: soft_skills.value,
    hobbies: hobbies.value,
    industry: industry.value,
    expectation: expectation.value
  };

  try {
    const res = await fetch("http://127.0.0.1:8000/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    output.innerText = data.result || data.error;
  } catch {
    output.innerText = "Unable to connect to server.";
  }

  btn.disabled = false;
  btn.innerText = "Generate Career Path →";
}