class ProductRecommender:
    """
    Maps YouCam Skin AI clinical diagnosis into targeted dermatological products
    and personalized AM/PM skincare routines with eCommerce cart links.
    """
    CATALOG = [
        {
            "id": "prod_hyaluronic_01",
            "name": "DermaPure 2% Multi-Molecular Hyaluronic Acid Serum",
            "category": "Hydration Booster",
            "target_metric": "hydration",
            "active_ingredient": "Hyaluronic Acid + B5",
            "price": 28.50,
            "rating": 4.8,
            "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&auto=format&fit=crop&q=60"
        },
        {
            "id": "prod_retinol_02",
            "name": "Clinical Pro-Retinoid 0.3% Anti-Wrinkle Treatment",
            "category": "Anti-Aging & Cellular Renewal",
            "target_metric": "wrinkles",
            "active_ingredient": "Encapsulated Retinal + Peptides",
            "price": 42.00,
            "rating": 4.9,
            "image_url": "https://images.unsplash.com/photo-1608248597359-5484809e59d9?w=400&auto=format&fit=crop&q=60"
        },
        {
            "id": "prod_niacinamide_03",
            "name": "Pore-Refining Niacinamide 10% + Zinc 1% Clarifying Serum",
            "category": "Texture & Tone Clarifier",
            "target_metric": "texture",
            "active_ingredient": "Niacinamide + Zinc PCA",
            "price": 24.00,
            "rating": 4.7,
            "image_url": "https://images.unsplash.com/photo-1617897903246-719242758050?w=400&auto=format&fit=crop&q=60"
        },
        {
            "id": "prod_caffeine_04",
            "name": "Eye Revive 5% Caffeine + EGCG Dark Circle Complex",
            "category": "Eye Contour Recovery",
            "target_metric": "dark_circles",
            "active_ingredient": "Green Tea EGCG + Caffeine",
            "price": 19.50,
            "rating": 4.6,
            "image_url": "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=400&auto=format&fit=crop&q=60"
        },
        {
            "id": "prod_vitamin_c_05",
            "name": "Radiance Brightening 15% L-Ascorbic Acid + Ferulic Acid",
            "category": "Spot & Hyperpigmentation Corrector",
            "target_metric": "spots",
            "active_ingredient": "Pure Vitamin C + Alpha Arbutin",
            "price": 36.00,
            "rating": 4.8,
            "image_url": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&auto=format&fit=crop&q=60"
        },
        {
            "id": "prod_cica_06",
            "name": "Centella Asiatica (Cica) Calming Barrier Repair Cream",
            "category": "Redness & Barrier Support",
            "target_metric": "redness",
            "active_ingredient": "Madecassoside + Ceramides",
            "price": 29.00,
            "rating": 4.9,
            "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&auto=format&fit=crop&q=60"
        }
    ]

    @classmethod
    def get_recommendations(cls, metrics: dict) -> dict:
        """
        Ranks products based on where the user has the lowest health scores.
        """
        scored_products = []
        for prod in cls.CATALOG:
            target = prod["target_metric"]
            metric_data = metrics.get(target, {"score": 75, "severity": "Normal"})
            score = metric_data["score"]
            # The lower the score, the higher the need for this product
            priority = 100 - score
            
            scored_products.append({
                **prod,
                "user_metric_score": score,
                "urgency_priority": priority,
                "severity_label": metric_data["severity"]
            })

        # Sort products by urgency (most needed first)
        scored_products.sort(key=lambda x: x["urgency_priority"], reverse=True)
        recommended = scored_products[:3]
        total_bundle_price = sum(p["price"] for p in recommended)
        bundle_discount_price = round(total_bundle_price * 0.85, 2) # 15% bundle discount

        routine = {
            "morning": [
                f"Gentle Cleanser + {recommended[0]['name']}",
                "Broad Spectrum SPF 50 Mineral Sunscreen"
            ],
            "evening": [
                "Double Cleanse Routine",
                f"Targeted Treatment: {recommended[1]['name'] if len(recommended) > 1 else recommended[0]['name']}",
                "Barrier Repair Moisturizer"
            ]
        }

        return {
            "primary_concern": recommended[0]["target_metric"].replace("_", " ").title(),
            "recommended_products": recommended,
            "bundle_price": bundle_discount_price,
            "original_price": round(total_bundle_price, 2),
            "savings": round(total_bundle_price - bundle_discount_price, 2),
            "routine": routine
        }
