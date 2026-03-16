import json

def event(type: str, **data) -> str:
    return f"data: {json.dumps({'type': type, **data})}\n\n"