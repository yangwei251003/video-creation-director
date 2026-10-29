"""Run OpenFilm's installed Codex adapter in the background, without desktop input."""
import json,os,subprocess,sys
from pathlib import Path
here=Path(__file__).resolve().parent
config=json.loads((here.parent/'local-environment.json').read_text(encoding='utf-8'))['openfilm']
env=dict(os.environ,ELECTRON_RUN_AS_NODE='1',OPENFILM_NO_UPDATE_CHECK='1')
flags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
result=subprocess.run([config['exe'],str(here/'openfilm_agent.mjs'),*sys.argv[1:]],env=env,creationflags=flags,capture_output=True,text=True,encoding='utf-8',errors='replace')
if result.stdout:print(result.stdout,end='')
if result.stderr:print(result.stderr,end='',file=sys.stderr)
raise SystemExit(result.returncode)
