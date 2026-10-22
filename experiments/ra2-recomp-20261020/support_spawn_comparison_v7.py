"""让实际中途出生的受控单位参与比较，不要求它在第 0 帧存在。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for name in ('run_fixture_comparison.py','run_state_comparison.py'):
    path = ROOT/name
    text = path.read_text(encoding='utf-8')
    assert 'original_samples =' not in text
    start = text.index("        lo = [next(o for o in r['objects']")
    end = text.index("        stop_frames =",start)
    text = text[:start]+'''        original_samples = [(r['frame'],o) for r in ls for o in r['objects'] if o['id']==uid]
        generated_samples = [(r['frame'],o) for r in rs for o in r['objects'] if o['id']==uid]
        if not original_samples or not generated_samples:
            raise ValueError('受控单位没有出现在状态轨迹中')
        sample_frames = [frame for frame,_ in original_samples]
        lo = [o for _,o in original_samples]
        ro = [o for _,o in generated_samples]
'''+text[end:]
    text = text.replace("for r, o in zip(ls, lo) if r['frame'] > last_stop)",
        "for frame, o in original_samples if frame > last_stop)")
    text = text.replace("last_stop is not None and len(ls) >= 10 and ls[-10]['frame'] > last_stop",
        "last_stop is not None and len(lo) >= 10 and sample_frames[-10] > last_stop and sample_frames[-1] == last")
    text = text.replace("'all_fields_equal': lo == ro,", "'all_fields_equal': original_samples == generated_samples,\n                           'first_observed_frame':sample_frames[0], 'last_observed_frame':sample_frames[-1],")
    path.write_text(text,encoding='utf-8',newline='\n')
