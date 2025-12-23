function analyze() {
  const fileInput = document.getElementById("imageInput");
  const file = fileInput.files[0];

  const formData = new FormData();
  formData.append("file", file);

  document.getElementById("preview").src = URL.createObjectURL(file);

  fetch("/analyze", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("result").innerHTML = `
      <p><b>Ingredient:</b> ${data.ingredient}</p>
      <p><b>Confidence:</b> ${data.confidence}</p>
      <p><b>OCR Text:</b> ${data.ocr_text || "None"}</p>
    `;
  });
}
