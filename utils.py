def format_display_value(p_data):
    if not p_data: return "N/A"
    meta = p_data.get('metadata', {})
    val_obj = p_data.get('value') or p_data.get('datavalue') or {}
    div = meta.get('divisor', 1) or 1
    val = val_obj.get('integerValue', 0) / div
    return f"{val:.{meta.get('decimal', 0)}f}"

def scale_value(val, divisor):
    return round(float(val) * (divisor or 1))