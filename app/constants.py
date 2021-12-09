import os
from pathlib import Path

FRAME_DATA_BUCKET = "webcam_data_scraping"
LABELED_FRAME_DATA_BUCKET = "labeled_webcam_data"

GOOD_PREFIX = "surf_quality_data/good"
FAIR_PREFIX = "surf_quality_data/fair"
POOR_PREFIX = "surf_quality_data/poor"


ACTIVE_PREFIX = "gating_data/visible"
INACTIVE_PREFIX = "gating_data/not_visible"


LOGO_PATH = Path("imgs/surfsight_logo.png")


if os.environ.get("CLASSIFICATION_PASSWORD"):
    CLASSIFICATION_PASSWORD = os.environ["CLASSIFICATION_PASSWORD"]
else:
    CLASSIFICATION_PASSWORD = "pass"
