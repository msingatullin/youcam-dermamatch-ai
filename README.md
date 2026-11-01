# DermaMatch AI — Clinical Skin Diagnostic & eCommerce Routine Recommender

**Submission for YouCam API Skin AI & eCommerce VTO Hackathon 2026**
*Prize Track: Total Cash Prizes ($6,000 USD)*
*Built by: Mikhail (@msingatullin)*

---

## 1. Executive Summary & Problem
Over 70% of consumers purchase skincare products that do not match their actual biological skin needs, resulting in high return rates and poor dermatological outcomes. Traditional eCommerce websites offer generic keyword searches rather than objective skin diagnostics.

**DermaMatch AI** bridges medical-grade computer vision with precision retail eCommerce. By integrating the **Perfect Corp YouCam Skin AI API**, the platform analyzes facial skin across 6 critical dimensions (Hydration, Wrinkles, Texture, Dark Circles, Spots, and Redness) and immediately maps diagnostic severity scores into a personalized 3-step active-ingredient regimen with 1-click bundle checkout.

---

## 2. Key Architecture & Features

```
[ User Selfie / Face Upload ]
             │
             ▼
[ YouCam Skin AI API (/ai-api) ]
├── Multitask Face Mesh Detection
├── Clinical Severity Indexing (6 Dimensions)
└── Biological Skin Age Estimation
             │
             ▼
[ Precision Product Recommender ]
├── Inverse Severity Priority Ranking
├── Ingredient Compatibility Engine (HA, Retinoids, Niacinamide)
└── AM/PM Clinical Regimen Formulation
             │
             ▼
[ Seamless eCommerce Cart & Checkout ]
└── 15% Dynamic Regimen Bundle Discount
```

- **YouCam API Integration:** Live endpoint connection to `https://yce.perfectcorp.com/api/v1/skin-analysis`.
- **Diagnostic Severity Mapping:** Dynamically scores skin health (0-100) and calculates biological skin age.
- **Formulation Matching:** Recommends targeted dermatological actives specifically addressing the user's primary concerns.
- **Frictionless eCommerce:** Instant bundle calculation, 15% regimen discount, and 1-click checkout.

---

## 3. Quick Start & Local Execution

```bash
# 1. Navigate to directory
cd youcam-dermamatch-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Configure Your YouCam API Key
export YOUCAM_API_KEY="your-perfectcorp-api-key"

# 4. Run Application
python main.py
```
Open `http://localhost:5050` in your web browser. Upload any face photo or click **"Use Demo Sample"** to trigger real-time AI scanning and product mapping.

---

## 4. Evaluation Rubric Compliance
- **API Integration:** Full integration with Perfect Corp YouCam Skin AI.
- **Consumer / Retail Value:** Direct eCommerce conversion channel reducing skincare return rates.
- **Design & Usability:** Clean, responsive clinical UI with real-time feedback and mobile support.
