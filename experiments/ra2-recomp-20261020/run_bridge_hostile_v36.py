"""Four bounded hostile bridge pairs in production or independent observation."""
from pathlib import Path
R=Path(__file__).resolve().parent
source=(R/'run_bridge_mixed_v36.py').read_text(encoding='utf-8')
source=source.replace('bridge-mixed-fixtures.json','bridge-hostile-fixtures.json').replace("'mh-'","'eh-'").replace("'mp-'","'ep-'")
exec(compile(source,str(Path(__file__)),'exec'),dict(__file__=str(Path(__file__)),__name__='__main__'))
