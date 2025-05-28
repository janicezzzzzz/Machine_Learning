const imageInput = document.getElementById('imageInput');
const preview = document.getElementById('preview');
const resultDiv = document.getElementById('result');

imageInput.onchange = () => {
  const file = imageInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = () => {
      preview.src = reader.result;
      preview.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
};

async function uploadImage() {
  const file = imageInput.files[0];
  if (!file) {
    alert("Please select an image first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  resultDiv.innerHTML = "Analyzing...";

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();

    resultDiv.innerHTML = `
      <strong>Flower:</strong> ${data.flower}<br>
      <strong>Meaning:</strong> ${data.meaning}
    `;
  } catch (error) {
    console.error("Error:", error);
    resultDiv.innerHTML = "Something went wrong. Try again.";
  }
}
