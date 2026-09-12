# -*- coding: utf-8 -*-
import json
import sys

with open('bdm_master_dataset.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

qs = d['questions']
with open('questions_summary.txt', 'w', encoding='utf-8') as out:
    for idx, q in enumerate(qs):
        corr = [o for o in q['options'] if o['is_correct']]
        c_lbl = corr[0]['label'] if corr else '?'
        c_txt = corr[0]['text'] if corr else '?'
        out.write(f"[{idx+1}] ID: {q['id']} | Src: {q['source']} | Wk: {q['week']}\n")
        out.write(f"Q: {q['question'].strip()}\n")
        for o in q['options']:
            star = " [*CORRECT*]" if o.get('is_correct') else ""
            out.write(f"   {o['label']}. {o['text'].strip()}{star}\n")
        if q.get('feedback'):
            out.write(f"Feedback: {q['feedback'].strip()}\n")
        out.write("-" * 60 + "\n")

print("Wrote questions_summary.txt successfully.")
