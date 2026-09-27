import json

with open('/Users/hzn/.gemini/antigravity/brain/2abf65d2-47cd-40ad-8511-68e97f8db32c/.system_generated/steps/4/content.md', 'r') as f:
    html = f.read()

start_idx = 0
while True:
    start_tag = '<script'
    end_tag = '</script>'
    s_idx = html.find(start_tag, start_idx)
    if s_idx == -1:
        break
    e_idx = html.find(end_tag, s_idx)
    if e_idx == -1:
        break
    script_content = html[s_idx:e_idx]
    start_idx = e_idx + len(end_tag)
    
    start_bracket = script_content.find('{')
    if start_bracket != -1:
        json_str = script_content[start_bracket:]
        try:
            data = json.loads(json_str)
            def find_text(obj):
                if isinstance(obj, dict):
                    if 'parts' in obj and isinstance(obj['parts'], list):
                        for p in obj['parts']:
                            if isinstance(p, str):
                                print("MESSAGE:", p[:200].replace('\n', ' '))
                    for k, v in obj.items():
                        find_text(v)
                elif isinstance(obj, list):
                    for item in obj:
                        find_text(item)
            find_text(data)
        except Exception as e:
            pass
