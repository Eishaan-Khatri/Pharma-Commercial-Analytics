from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"
SAMPLE_DIR = DATA_DIR / "sample"
OUTPUT_DIR = ROOT / "outputs"
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"
DASHBOARD_DIR = ROOT / "dashboards" / "screenshots"
REPORTS_DIR = ROOT / "reports"

SAMPLE_DATA_PATH = SAMPLE_DIR / "pharma_transactions_sample.csv"
CLEAN_DATA_PATH = SAMPLE_DIR / "pharma_transactions_clean.csv"

RANDOM_SEED = 42

DRUG_CATEGORIES = [
    "Analgesics", "Antibiotics", "Antivirals", "Antifungals", "Antihistamines",
    "Antidiabetics", "Cardiology", "Hypertension", "Lipid Management",
    "Gastrointestinal", "Respiratory", "Dermatology", "Oncology Support",
    "Vitamins", "Minerals", "Neurology", "Psychiatry", "Ophthalmology",
    "ENT", "Urology", "Nephrology", "Hepatology", "Rheumatology",
    "Endocrinology", "Women Health", "Pediatrics", "Geriatrics",
    "Emergency Care", "Vaccines", "Pain Management", "Cough Cold",
    "Allergy", "Anti-inflammatory", "Anticoagulants", "Antiplatelets",
    "Diuretics", "Hormonal Therapy", "Insulin", "Oral Rehydration",
    "Wound Care", "Dental Care", "Medical Nutrition", "Critical Care",
    "Anesthesia", "Diagnostic Aids", "Immunology", "Bone Health",
    "Anti-malarial", "Anti-tubercular", "Fertility", "Sleep Care",
    "Smoking Cessation", "Weight Management", "Renal Care",
    "Liver Care", "Probiotics", "Rare Disease"
]

REGIONS = ["North", "South", "East", "West", "Central"]
CHANNELS = ["Retail", "Hospital", "Distributor", "Online", "Government"]
CUSTOMER_SEGMENTS = [
    "Tier-1 Hospitals",
    "Tier-2 Clinics",
    "Retail Chains",
    "Independent Pharmacies",
    "Public Health",
    "Specialty Centers",
]

def ensure_directories() -> None:
    for path in [SAMPLE_DIR, OUTPUT_DIR, TABLES_DIR, FIGURES_DIR, DASHBOARD_DIR, REPORTS_DIR]:
        path.mkdir(parents=True, exist_ok=True)

