from pathlib import Path
from typing import Final

ROOT: Final = Path(__file__).resolve().parents[2]
FAMILY_ROOT: Final = ROOT / "contracts" / "council-convening"
FIXTURE_ROOT: Final = FAMILY_ROOT / "fixtures"
INDEX_PATH: Final = FIXTURE_ROOT / "index.yaml"
SCHEMA_PATH: Final = FAMILY_ROOT / "resolved-council-convening.schema.yaml"
INDEX_RELATIVE_PATH: Final = "contracts/council-convening/fixtures/index.yaml"
SCHEMA_RELATIVE_PATH: Final = "contracts/council-convening/resolved-council-convening.schema.yaml"
