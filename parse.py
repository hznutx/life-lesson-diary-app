import json
import re

with open('/Users/hzn/.gemini/antigravity/brain/2abf65d2-47cd-40ad-8511-68e97f8db32c/.system_generated/steps/4/content.md', 'r') as f:
    html = f.read()

scripts2 = re.findall(r'<script[^>]*type=[\"\'\']application/json[\"\'\'][^>]*>(.*?)</script>', html, re.DOTALL)
for i, s in enumerate(scripts2):
    if len(s) > 1000:
        print(f'Found application/json blob {i}, length {len(s)}')
        try:
            data = json.loads(s)
            print('Successfully parsed as JSON')
            
            # recursive function to find all string values that might be chat text
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
            print(e)
