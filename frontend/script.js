async function searchProducts() {
  const query = document.getElementById("searchInput").value;

  if (!query) return;

  const loadingEl = document.getElementById("loading");
  const resultsEl = document.getElementById("results");
  const aiEl = document.getElementById("ai-output");

  loadingEl.innerText = "Looking through the shelves…";
  resultsEl.innerHTML = "";
  aiEl.innerHTML = "";

  try {
    const params = new URLSearchParams({ query });
    const res = await fetch(`http://127.0.0.1:8000/search/?${params.toString()}`, {
      method: "POST",
    });

    const data = await res.json();

    console.log("API Response:", data);

    displayProducts(data.products);
    displayAI(data.final);
  } catch (err) {
    console.error(err);
    loadingEl.innerText = "Couldn't fetch results. Please try again.";
    return;
  }

  loadingEl.innerText = "";
}

function displayProducts(products) {
  const container = document.getElementById("results");

  if (!products || products.length === 0) {
    container.innerHTML = `<p class="empty-state">No products found — try a different search.</p>`;
    return;
  }

  products.forEach((p) => {
    const div = document.createElement("div");
    div.className = "card";

    div.innerHTML = `
      <img src="${p.image}" alt="${p.name}" loading="lazy">
      <h3>${p.name}</h3>
      <p class="price">₹${p.price}</p>
      <p class="rating">⭐ ${p.rating}</p>
      <p class="score">Match score: ${p.score?.toFixed(2)}</p>
    `;

    container.appendChild(div);
  });
}

function displayAI(text) {
  const box = document.getElementById("ai-output");

  if (!text) return;

  box.innerHTML = `
    <h3>🤖 AI Recommendation</h3>
    <p>${text}</p>
  `;
}

// Allow pressing Enter in the search box
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("searchInput");
  if (input) {
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") searchProducts();
    });
  }
});