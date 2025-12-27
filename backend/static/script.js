// ===== Milestone 1: Image → CNN + OCR =====
async function analyzeImage() {
  const file = document.getElementById("imageInput").files[0];
  if (!file) {
    alert("Please upload an image");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("/analyze", {
    method: "POST",
    body: formData
  });

  const data = await res.json();

  const cnnNames = data.cnn_ingredients.map(i => i.name);

  document.getElementById("analysisResult").innerHTML = `
    <p><b>CNN Ingredients:</b> ${cnnNames.join(", ")}</p>
    <p><b>OCR Text:</b> ${data.ocr_ingredients}</p>
  `;

  // 🔥 Auto-fill ingredient box
  document.getElementById("ingredientsInput").value = cnnNames.join(",");
}

// ===== Milestone 2: Ingredients → Recipes =====
async function getRecipes() {
  const raw = document.getElementById("ingredientsInput").value;
  const ingredients = raw.split(",").map(i => i.trim());

  const res = await fetch("/recommend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ingredients)
  });

  const data = await res.json();

  const list = document.getElementById("recipeResults");
  list.innerHTML = "";

  data.forEach(r => {
    const li = document.createElement("li");
    li.innerText = `${r.recipe} — ${r.match_percentage}% match`;
    list.appendChild(li);
  });
}
