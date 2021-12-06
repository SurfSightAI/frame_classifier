import os
from pathlib import Path

FRAME_DATA_BUCKET = "webcam_data_scraping"
LABELED_FRAME_DATA_BUCKET = "labeled_webcam_data"

GLASSY_PREFIX = "surf_quality_data/glassy"
SEMI_CHOP_PREFIX = "surf_quality_data/semi_chop"
CHOPPY_PREFIX = "surf_quality_data/choppy"


ACTIVE_PREFIX = "gating_data/visible"
INACTIVE_PREFIX = "gating_data/not_visible"


LOGO_PATH = Path("imgs/surfsight_logo.png")


if os.environ.get("CLASSIFICATION_PASSWORD"):
    CLASSIFICATION_PASSWORD = os.environ["CLASSIFICATION_PASSWORD"]
else:
    CLASSIFICATION_PASSWORD = 'pass'
