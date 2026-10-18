from pathlib import Path
import json,shutil
root=Path(__file__).resolve().parents[1]
db=json.loads((root/'src/conteudo.json').read_text(encoding='utf-8'))
payload=json.dumps(db,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
template=(root/'src/app_v2.template.html').read_text(encoding='utf-8')
assert '__DATA__' in template
public=root/'public'
(public/'data').mkdir(parents=True,exist_ok=True)
(public/'index.html').write_text(template.replace('__DATA__',payload),encoding='utf-8')
(public/'data/conteudo.json').write_text(json.dumps(db,ensure_ascii=False,indent=2),encoding='utf-8')
print('Build OK', (public/'index.html').stat().st_size, 'bytes')
