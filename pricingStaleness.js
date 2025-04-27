from datetime import datetime, timedelta

def is_data_stale(doc):
    last_updated = doc.get("last_updated")
    if not last_updated:
        return False
    last_updated_dt = datetime.fromisoformat(last_updated.rstrip('Z'))
    return (datetime.utcnow() - last_updated_dt) > timedelta(days=90)
