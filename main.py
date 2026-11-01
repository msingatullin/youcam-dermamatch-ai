import os
from flask import Flask, render_template, request, jsonify
from app.youcam_client import YouCamSkinAIClient
from app.product_recommender import ProductRecommender

app = Flask(__name__)
youcam_client = YouCamSkinAIClient()

@app.route("/")
def index():
    return render_template("index.html", catalog=ProductRecommender.CATALOG)

@app.route("/api/analyze", methods=["POST"])
def analyze_skin():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    img_bytes = file.read()
    if len(img_bytes) == 0:
        return jsonify({"error": "Empty file contents"}), 400

    # 1. Run YouCam AI diagnostic
    diagnostic = youcam_client.analyze_skin_image(img_bytes)

    # 2. Map to personalized eCommerce products & routine
    recommendations = ProductRecommender.get_recommendations(diagnostic["metrics"])

    return jsonify({
        "diagnostic": diagnostic,
        "recommendations": recommendations
    })

@app.route("/api/checkout", methods=["POST"])
def checkout():
    data = request.json or {}
    items = data.get("items", [])
    total = data.get("total", 0.0)
    order_id = f"ORDER-{os.urandom(4).hex().upper()}"
    return jsonify({
        "success": True,
        "order_id": order_id,
        "items_count": len(items),
        "charged_amount": total,
        "message": f"Order #{order_id} placed successfully! Your personalized skincare regimen is being prepared."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
