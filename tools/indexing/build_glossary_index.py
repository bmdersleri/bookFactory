#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from datetime import datetime, UTC
from typing import Any
from tools.utils.yaml_utils import load_yaml
FM=re.compile(r"\A---\s*\n.*?\n---\s*\n",re.S); CODE=re.compile(r"```.*?```",re.S); COM=re.compile(r"<!--.*?-->",re.S)
GH=re.compile(r"^(#{2,6})\s+(.*?(terim\s+sözlüğü|glossary).*)$",re.I|re.M); SEP=re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
def base_for(profile_path, profile):
    pr=profile.get('project_root') or profile.get('post_production',{}).get('project_root')
    if pr:
        pp=Path(str(pr)); return pp.resolve() if pp.is_absolute() else (profile_path.parent/pp).resolve()
    return Path.cwd().resolve()
def resolve(base,v):
    p=Path(str(v)); return p if p.is_absolute() else (base/p).resolve()
def strip(text): return FM.sub('',text,1)
def clean(text): return COM.sub('\n',CODE.sub('\n',text))
def row(line): return [c.strip().replace('<br>',' ') for c in line.strip().strip('|').split('|')]
def section_end(text,start,level):
    for m in re.finditer(r'^(#{1,6})\s+',text[start:],re.M):
        if len(m.group(1))<=level: return start+m.start()
    return len(text)
def entries(profile,base):
    out=[]
    for i,ch in enumerate(profile.get('chapters') or [],1):
        if not isinstance(ch,dict) or not (ch.get('source') or ch.get('path')): continue
        out.append({'order':int(ch.get('order') or i),'chapter_id':str(ch.get('chapter_id') or ch.get('id') or f'chapter_{i:02d}'),'source':str(ch.get('source') or ch.get('path')),'path':resolve(base,ch.get('source') or ch.get('path'))})
    return sorted(out,key=lambda x:x['order'])
def extract(text,ch):
    text=strip(text); items=[]
    for hm in GH.finditer(text):
        sec=text[hm.end():section_end(text,hm.end(),len(hm.group(1)))]
        lines=sec.splitlines(); i=0
        while i < len(lines):
            if '|' not in lines[i] or i+1>=len(lines) or not SEP.match(lines[i+1]): i+=1; continue
            headers=[h.casefold() for h in row(lines[i])]; tc=0; dc=1 if len(headers)>1 else 0
            for n,h in enumerate(headers):
                if any(t in h for t in ['terim','term','kavram']): tc=n
                if any(t in h for t in ['açıklama','aciklama','definition','tanım','tanim']): dc=n
            i+=2
            while i<len(lines) and '|' in lines[i]:
                cells=row(lines[i])
                if len(cells)>max(tc,dc):
                    term=re.sub(r'[`*_]','',cells[tc]).strip(); definition=re.sub(r'[`*_]','',cells[dc]).strip()
                    if term: items.append({'term':term,'definition':definition,'chapter_id':ch['chapter_id'],'chapter_order':ch['order'],'section':hm.group(2).strip(),'source':ch['source']})
                i+=1
    return items
def slug(s):
    return re.sub(r'[^a-z0-9]+','-',s.translate(str.maketrans({'ı':'i','ğ':'g','ü':'u','ş':'s','ö':'o','ç':'c','İ':'i'})).casefold()).strip('-') or 'term'
def merge(raw):
    d={}
    for it in raw:
        key=re.sub(r'\s+',' ',it['term'].casefold().strip()); cur=d.setdefault(key,{'term':it['term'],'slug':slug(it['term']),'definition':it.get('definition',''),'references':[]})
        ref={k:it[k] for k in ['chapter_id','chapter_order','section','source']}
        if ref not in cur['references']: cur['references'].append(ref)
    return sorted(d.values(),key=lambda x:x['term'].casefold())
def refs(term,chapters):
    pat=re.compile(re.escape(term),re.I); out=[]; total=0
    for ch in chapters:
        if not ch['path'].exists(): continue
        txt=clean(strip(ch['path'].read_text(encoding='utf-8'))); heads=[(m.start(),m.group(2).strip()) for m in re.finditer(r'^(#{1,6})\s+(.+?)\s*$',txt,re.M)]; secs={}
        for m in pat.finditer(txt):
            if len(term)<=3:
                b=txt[m.start()-1] if m.start()>0 else ' '; a=txt[m.end()] if m.end()<len(txt) else ' '
                if b.isalnum() or a.isalnum(): continue
            h=ch['chapter_id']
            for pos,title in heads:
                if pos<=m.start(): h=title
                else: break
            secs[h]=secs.get(h,0)+1; total+=1
        for s,c in secs.items(): out.append({'chapter_order':ch['order'],'chapter_id':ch['chapter_id'],'section':s,'occurrences':c})
    return total,out
def md_gloss(g):
    lines=['# Terim Sözlüğü','','| Terim | Açıklama | Referanslar |','|---|---|---|']
    for it in g:
        r=', '.join(dict.fromkeys([f"Bölüm {x['chapter_order']} ({x['chapter_id']})" for x in it['references']]))
        lines.append(f"| {it['term']} | {it.get('definition','')} | {r} |")
    return '\n'.join(lines)+'\n'
def md_index(items):
    lines=['# Arka Dizin','','Bu dizin sayfa numarası yerine bölüm ve başlık referansları kullanır.','']; cur=''
    for it in items:
        f=it['term'][:1].upper()
        if f!=cur: cur=f; lines += [f'## {cur}','']
        rs='; '.join([f"Bölüm {r['chapter_order']} — {r['section']} ({r['occurrences']})" for r in it['references']]) or 'Referans bulunamadı'
        lines.append(f"- **{it['term']}** — {rs}")
    return '\n'.join(lines)+'\n'
def review(g,idx): return '# Glossary and Index Review Prompt\n\nTerim sözlüğü ve arka dizin deterministik olarak üretildi. Teknik editör olarak tekrar eden terimleri, eksik tanımları ve referansların yeterliliğini değerlendir.\n\n- Terim sayısı: '+str(len(g))+'\n- Dizin girdisi sayısı: '+str(len(idx))+'\n'
_GLOSS_MARKER = '<!-- BOOKFACTORY_GLOSSARY_START -->'

def append_glossary_to_merged(merged_md: Path, glossary_text: str) -> None:
    text = merged_md.read_text(encoding='utf-8') if merged_md.exists() else ''
    # Önceki glossary varsa kaldır
    if _GLOSS_MARKER in text:
        text = text[:text.index(_GLOSS_MARKER)].rstrip()
    appendix = f'\n\n\\newpage\n\n{_GLOSS_MARKER}\n\n{glossary_text.strip()}\n'
    merged_md.write_text(text + appendix, encoding='utf-8')
    print(f'[OK] Terim sözlüğü merged markdown\'a eklendi: {merged_md}')

def build(profile_path:Path, output_dir:Path|None, fail_on_empty:bool, append_to_merged:bool=False)->int:
    profile=load_yaml(profile_path); base=base_for(profile_path,profile); out=output_dir or Path(str((profile.get('indexing') or {}).get('output_dir') or 'build/index')); out=out if out.is_absolute() else (base/out).resolve()
    chapters=entries(profile,base); raw=[]; existing=[]; warnings=[]
    for ch in chapters:
        if ch['path'].exists(): existing.append(ch); raw += extract(ch['path'].read_text(encoding='utf-8'),ch)
        else: warnings.append('Missing chapter: '+ch['source'])
    g=merge(raw)
    if not g:
        warnings.append("No glossary table entries found.")
        if fail_on_empty: print('[ERROR] No glossary entries found.',file=sys.stderr); return 1
    idx=[]
    for it in g:
        total,r=refs(it['term'],existing); idx.append({'term':it['term'],'slug':it['slug'],'total_occurrences':total,'references':r})
    idx=sorted(idx,key=lambda x:x['term'].casefold()); out.mkdir(parents=True,exist_ok=True)
    gp={'schema_version':'2.8.0','terms':g}; ip={'schema_version':'2.8.0','terms':idx}
    (out/'glossary.json').write_text(json.dumps(gp,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); (out/'book_index.json').write_text(json.dumps(ip,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'glossary.yaml').write_text(json.dumps(gp,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); (out/'book_index.yaml').write_text(json.dumps(ip,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    gloss_text=md_gloss(g)
    (out/'glossary.md').write_text(gloss_text,encoding='utf-8'); (out/'book_index.md').write_text(md_index(idx),encoding='utf-8'); (out/'glossary_index_review_prompt.md').write_text(review(g,idx),encoding='utf-8')
    rep={'schema_version':'2.8.0','generated_at':datetime.now(UTC).isoformat(timespec='seconds').replace('+00:00','Z'),'chapters_scanned':len(existing),'raw_glossary_entries':len(raw),'unique_glossary_terms':len(g),'index_terms':len(idx),'warnings':warnings}
    (out/'indexing_report.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    text=f"# Glossary / Index Build Report\n\n- Generated at: `{rep['generated_at']}`\n- Chapters scanned: `{rep['chapters_scanned']}`\n- Raw glossary entries: `{rep['raw_glossary_entries']}`\n- Unique glossary terms: `{rep['unique_glossary_terms']}`\n- Index terms: `{rep['index_terms']}`\n"
    (out/'indexing_report.md').write_text(text,encoding='utf-8'); print(text)
    if append_to_merged:
        pp=profile.get('post_production',{}); bld=pp.get('build',{})
        md_rel=bld.get('merged_markdown') or 'build/merged/book_merged.md'
        cwd_base=Path.cwd().resolve()
        merged_md=Path(md_rel) if Path(md_rel).is_absolute() else (cwd_base/md_rel).resolve()
        if merged_md.exists(): append_glossary_to_merged(merged_md, gloss_text)
        else: print(f'[WARN] Merged markdown bulunamadı, atlandı: {merged_md}', file=sys.stderr)
    return 0
def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument('--profile',type=Path,required=True); p.add_argument('--output-dir',type=Path); p.add_argument('--fail-on-empty',action='store_true'); p.add_argument('--append-to-merged',action='store_true',help='Terim sözlüğünü merged markdown dosyasına ekle'); a=p.parse_args(argv); return build(a.profile.resolve(),a.output_dir,a.fail_on_empty,a.append_to_merged)
if __name__=='__main__': raise SystemExit(main())
