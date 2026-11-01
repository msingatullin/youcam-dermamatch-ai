let currentAnalysis = null;

document.addEventListener("DOMContentLoaded", () => {
    const imageInput = document.getElementById("image-input");
    const btnDemo = document.getElementById("btn-demo-sample");

    imageInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) handleFile(file);
    });

    btnDemo.addEventListener("click", () => {
        // Create a 1x1 test blob to trigger demo analysis
        fetch("https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&auto=format&fit=crop&q=60")
            .then(res => res.blob())
            .then(blob => {
                const file = new File([blob], "demo_face.jpg", { type: "image/jpeg" });
                handleFile(file);
            })
            .catch(() => {
                // Fallback local synthetic canvas
                const canvas = document.createElement("canvas");
                canvas.width = 100;
                canvas.height = 100;
                canvas.toBlob(blob => {
                    const file = new File([blob], "demo_face.jpg", { type: "image/jpeg" });
                    handleFile(file);
                });
            });
    });
});

function handleFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById("image-preview").src = e.target.result;
        document.getElementById("upload-prompt").style.display = "none";
        document.getElementById("preview-container").style.display = "block";
    };
    reader.readAsDataURL(file);

    const formData = new FormData();
    formData.append("image", file);

    fetch("/api/analyze", {
        method: "POST",
        body: formData
    })
    .then(r => r.json())
    .then(data => {
        currentAnalysis = data;
        displayResults(data);
    })
    .catch(err => alert("Analysis error: " + err));
}

function resetUpload() {
    document.getElementById("upload-prompt").style.display = "block";
    document.getElementById("preview-container").style.display = "none";
    document.getElementById("results-section").style.display = "none";
    document.getElementById("image-input").value = "";
}

function displayResults(data) {
    const diag = data.diagnostic;
    const rx = data.recommendations;

    document.getElementById("results-section").style.display = "flex";
    document.getElementById("overall-score").innerText = diag.overall_skin_score;
    document.getElementById("skin-age").innerText = diag.estimated_skin_age + " yrs";
    document.getElementById("primary-concern").innerText = "Primary Concern: " + rx.primary_concern;

    // Populate metrics
    for (const [key, val] of Object.entries(diag.metrics)) {
        const textEl = document.getElementById("m-" + key);
        const barEl = document.getElementById("bar-" + key);
        if (textEl && barEl) {
            textEl.innerText = val.score + "% (" + val.severity + ")";
            barEl.style.width = val.score + "%";
            barEl.style.background = val.score < 50 ? "#EF4444" : (val.score < 70 ? "#F59E0B" : "#0F766E");
        }
    }

    // Populate products
    const prodContainer = document.getElementById("products-container");
    prodContainer.innerHTML = rx.recommended_products.map(p => `
        <div class="product-card">
            <img src="${p.image_url}" alt="${p.name}">
            <span class="prod-cat">${p.category}</span>
            <div class="prod-title">${p.name}</div>
            <div class="prod-active">Active: ${p.active_ingredient}</div>
            <div class="prod-bottom">
                <span class="prod-price">$${p.price.toFixed(2)}</span>
                <span style="font-size:12px; color:#10B981; font-weight:700;">★ ${p.rating}</span>
            </div>
        </div>
    `).join("");

    // Populate bundle checkout
    document.getElementById("original-price").innerText = "$" + rx.original_price.toFixed(2);
    document.getElementById("final-price").innerText = "$" + rx.bundle_price.toFixed(2);
}

function performCheckout() {
    if (!currentAnalysis) return;
    const btn = document.getElementById("btn-checkout");
    btn.innerText = "⏳ Processing...";
    btn.disabled = true;

    fetch("/api/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            items: currentAnalysis.recommendations.recommended_products,
            total: currentAnalysis.recommendations.bundle_price
        })
    })
    .then(r => r.json())
    .then(res => {
        alert("🎉 " + res.message);
    })
    .finally(() => {
        btn.innerText = "🛒 1-Click Bundle Checkout";
        btn.disabled = false;
    });
}
