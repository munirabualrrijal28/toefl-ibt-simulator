import requests

BASE = "http://localhost:8000"
sid = requests.post(f"{BASE}/session/start").json()["id"]
print(f"Session: {sid}\n")

seen_ids = []
seen_texts = []

for i in range(12):
    try:
        state = requests.get(f"{BASE}/session/{sid}/current-state").json()
        item = requests.get(f"{BASE}/session/{sid}/next-item").json()
    except Exception as e:
        print(f"Q{i+1}: Test complete or error: {e}")
        break

    qid = item["id"]
    meta = item.get("content_meta", {})
    text = (meta.get("passage") or meta.get("transcript") or meta.get("prompt") or meta.get("phrase") or "N/A")[:60]
    
    id_dup = "ID-DUPLICATE!" if qid in seen_ids else "OK"
    text_dup = "TEXT-DUPLICATE!" if text in seen_texts else "unique"
    
    seen_ids.append(qid)
    seen_texts.append(text)
    
    section = state.get("section_name", "?")
    stage = state.get("stage", "?")
    task_type = item.get("task_type", "?")
    
    print(f"Q{i+1}: [{section}/{stage}] {task_type} | {id_dup} | {text_dup}")
    print(f"      Text: {text}...")
    
    requests.post(f"{BASE}/session/{sid}/submit-response", json={"question_id": qid, "text_payload": "test"})

print(f"\n=== RESULTS ===")
print(f"Total questions: {len(seen_ids)}")
print(f"Unique IDs: {len(set(seen_ids))}")
print(f"Unique texts: {len(set(seen_texts))}")
print(f"ID Duplicates: {len(seen_ids) - len(set(seen_ids))}")
print(f"Text Duplicates: {len(seen_texts) - len(set(seen_texts))}")
