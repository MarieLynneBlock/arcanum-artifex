import pathlib, re, subprocess, sys
root = pathlib.Path('/Users/lien/Code/AI_Code/arcanum-artifex/workflows/4plus1-diagrams/templates/drawio')
validator = pathlib.Path('/Users/lien/Code/AI_Code/arcanum-artifex/workflows/4plus1-diagrams/skills/draw-io-diagram-generator/scripts/validate-drawio.py')
cell = '''        <mxCell id="canonical-source-ref" value="canonical-source-path=&lt;path&gt;&#10;canonical-source-format=&lt;mmd|puml&gt;&#10;canonical-source-summary=&lt;short summary&gt;" style="text;strokeColor=none;fillColor=none;opacity=0;html=1;" vertex="1" parent="1">
          <mxGeometry x="0" y="0" width="1" height="1" as="geometry" />
        </mxCell>\n'''
for f in sorted(root.glob('*.drawio')):
    s = f.read_text()
    if 'id="canonical-source-ref"' in s:
        print(f'SKIP {f.name} (already has provenance)')
        continue
    new = re.sub(r'(?P<i>[ \t]*)</root>', lambda m: cell + m.group('i') + '</root>', s, count=1)
    if new == s:
        print(f'NO MATCH {f.name}'); sys.exit(2)
    f.write_text(new)
    print(f'INJECTED {f.name}')
print('--- validate ---')
fail = 0
for f in sorted(root.glob('*.drawio')):
    r = subprocess.run(['python', str(validator), str(f), '--require-provenance'], capture_output=True, text=True)
    print(f.name, '->', 'OK' if r.returncode == 0 else 'FAIL')
    if r.returncode != 0:
        print(r.stdout); print(r.stderr); fail += 1
sys.exit(fail)
