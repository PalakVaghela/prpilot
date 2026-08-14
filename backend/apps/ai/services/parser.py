import json


def parser_ai_response(res):
    res = res.strip()
    if res.startswith("```json"):
        res = res[7:]
    if res.endswith("```"):
        res = res[:-3]
    res = res.strip()
    return json.loads(res)
