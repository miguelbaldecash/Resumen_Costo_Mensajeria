"""
Actualizar JS de datos del dashboard hasta Jul 7, 2026.
- Completa junio (dias 24-30) con datos de DB + AC
- Agrega julio 1-7 como nuevo mes
"""
import json
from collections import defaultdict

MONTHS = ["ene", "feb", "mar", "abr", "may", "jun", "jul"]
MONTH_IDX = {"ene": 3, "feb": 4, "mar": 5, "abr": 6, "may": 7, "jun": 8, "jul": 9}

# ============================================================
# Load extracts
# ============================================================
print("Loading extracts...")
with open("_db_new_extract.json") as f:
    db = json.load(f)
with open("_ac_new_data.json") as f:
    ac = json.load(f)

# ============================================================
# Load existing template_data.js
# ============================================================
print("Loading existing template_data.js...")
with open("template_data.js", "r", encoding="utf-8") as f:
    raw = f.read()
prefix = "const templateData = "
old_data = json.loads(raw[len(prefix):].rstrip().rstrip(";"))

# Build lookup: (provider, template_name) -> row index
old_lookup = {}
for i, row in enumerate(old_data):
    old_lookup[(row[0], row[1])] = i

# Current format: [provider, name, category, ene, feb, mar, abr, may, jun, total, meta]
# New format:     [provider, name, category, ene, feb, mar, abr, may, jun, jul, total, meta]

# ============================================================
# 1. Extend all existing rows to include jul column
# ============================================================
print("\n=== Extending data to include julio ===")
new_data = []
for row in old_data:
    # Insert jul=0 before total, update total position
    new_row = row[:9] + [0, row[9], row[10]]
    # row indices: 0=prov, 1=name, 2=cat, 3=ene, 4=feb, 5=mar, 6=abr, 7=may, 8=jun, 9=jul, 10=total, 11=meta
    new_data.append(new_row)

# Rebuild lookup with new_data
lookup = {}
for i, row in enumerate(new_data):
    lookup[(row[0], row[1])] = i

# ============================================================
# 2. Add DB delta for Jun 24-30
# ============================================================
print("\n=== Adding Jun 24-30 DB data ===")
jun_added = 0
jun_new_templates = 0

for tpl_name, cnt in db["blip_jun_new"]:
    key = ("blip", tpl_name)
    if key in lookup:
        new_data[lookup[key]][8] += cnt  # jun column
        jun_added += cnt
    else:
        # New template not seen before
        row = ["blip", tpl_name, "sin_clasificar", 0, 0, 0, 0, 0, cnt, 0, 0, "MARKETING"]
        new_data.append(row)
        lookup[key] = len(new_data) - 1
        jun_added += cnt
        jun_new_templates += 1

for tpl_name, cnt in db["vox_jun_new"]:
    key = ("voximplant", tpl_name)
    if key in lookup:
        new_data[lookup[key]][8] += cnt
        jun_added += cnt
    else:
        row = ["voximplant", tpl_name, "cobranza_mora", 0, 0, 0, 0, 0, cnt, 0, 0, "MARKETING"]
        new_data.append(row)
        lookup[key] = len(new_data) - 1
        jun_added += cnt
        jun_new_templates += 1

print(f"  Jun 24-30 DB: +{jun_added:,} msgs, {jun_new_templates} new templates")

# ============================================================
# 3. Add AC delta for Jun 24-30
# ============================================================
print("\n=== Adding Jun 24-30 AC retargeting ===")
ac_jun_added = 0
ac_jun_new = 0

for tpl_name, months in ac["tpl_month"].items():
    jun_cnt = months.get("jun", 0)
    if jun_cnt == 0:
        continue
    key = ("blip", tpl_name)
    if key in lookup:
        new_data[lookup[key]][8] += jun_cnt
        ac_jun_added += jun_cnt
    else:
        row = ["blip", tpl_name, "retargeting", 0, 0, 0, 0, 0, jun_cnt, 0, 0, "MARKETING"]
        new_data.append(row)
        lookup[key] = len(new_data) - 1
        ac_jun_added += jun_cnt
        ac_jun_new += 1

print(f"  Jun 24-30 AC: +{ac_jun_added:,} msgs, {ac_jun_new} new templates")

# ============================================================
# 4. Add Jul 1-7 DB data
# ============================================================
print("\n=== Adding Jul 1-7 DB data ===")
jul_added = 0
jul_new_templates = 0

for tpl_name, cnt in db["blip_jul"]:
    key = ("blip", tpl_name)
    if key in lookup:
        new_data[lookup[key]][9] += cnt  # jul column
        jul_added += cnt
    else:
        row = ["blip", tpl_name, "sin_clasificar", 0, 0, 0, 0, 0, 0, cnt, 0, "MARKETING"]
        new_data.append(row)
        lookup[key] = len(new_data) - 1
        jul_added += cnt
        jul_new_templates += 1

for tpl_name, cnt in db["vox_jul"]:
    key = ("voximplant", tpl_name)
    if key in lookup:
        new_data[lookup[key]][9] += cnt
        jul_added += cnt
    else:
        row = ["voximplant", tpl_name, "cobranza_mora", 0, 0, 0, 0, 0, 0, cnt, 0, "MARKETING"]
        new_data.append(row)
        lookup[key] = len(new_data) - 1
        jul_added += cnt
        jul_new_templates += 1

print(f"  Jul 1-7 DB: +{jul_added:,} msgs, {jul_new_templates} new templates")

# ============================================================
# 5. Add Jul 1-7 AC retargeting
# ============================================================
print("\n=== Adding Jul 1-7 AC retargeting ===")
ac_jul_added = 0
ac_jul_new = 0

for tpl_name, months in ac["tpl_month"].items():
    jul_cnt = months.get("jul", 0)
    if jul_cnt == 0:
        continue
    key = ("blip", tpl_name)
    if key in lookup:
        new_data[lookup[key]][9] += jul_cnt
        ac_jul_added += jul_cnt
    else:
        row = ["blip", tpl_name, "retargeting", 0, 0, 0, 0, 0, 0, jul_cnt, 0, "MARKETING"]
        new_data.append(row)
        lookup[key] = len(new_data) - 1
        ac_jul_added += jul_cnt
        ac_jul_new += 1

print(f"  Jul 1-7 AC: +{ac_jul_added:,} msgs, {ac_jul_new} new templates")

# ============================================================
# 6. Recalculate totals and sort
# ============================================================
print("\n=== Recalculating totals ===")
for row in new_data:
    row[10] = sum(row[3:10])  # total = ene+feb+mar+abr+may+jun+jul

# Remove rows with 0 total
new_data = [r for r in new_data if r[10] > 0]
new_data.sort(key=lambda x: -x[10])

print(f"  Total templates: {len(new_data)}")
for m in MONTHS:
    idx = MONTH_IDX[m]
    total = sum(row[idx] for row in new_data)
    print(f"  {m}: {total:,} msgs")

# Write template_data.js
with open("template_data.js", "w", encoding="utf-8") as f:
    f.write("const templateData = " + json.dumps(new_data, ensure_ascii=False) + ";")
print("  Written template_data.js")

# ============================================================
# 7. BUILD template_totals.js
# ============================================================
print("\n=== Rebuilding template_totals.js ===")

totals = {}
for m in MONTHS:
    idx = MONTH_IDX[m]
    by_area = defaultdict(int)
    by_meta = defaultdict(int)
    grand = 0
    for row in new_data:
        v = row[idx]
        if v > 0:
            by_area[row[2]] += v
            by_meta[row[11]] += v
            grand += v
    totals[m] = {
        "grand": grand,
        "byArea": dict(by_area),
        "byMeta": dict(by_meta)
    }
    print(f"  {m}: grand={grand:,}")

with open("template_totals.js", "w", encoding="utf-8") as f:
    f.write("const templateTotals = " + json.dumps(totals, ensure_ascii=False) + ";")
print("  Written template_totals.js")

# ============================================================
# 8. UPDATE phone_inline.js (add jul)
# ============================================================
print("\n=== Updating phone_inline.js ===")

with open("phone_inline.js", "r", encoding="utf-8") as f:
    raw = f.read()
phone_data = json.loads(raw[len("const allPhoneData = "):].rstrip().rstrip(";"))

# Add jun 24-30 phones to existing jun data
jun_phones = {row[0]: row for row in phone_data.get("jun", [])}
for tpl, phone, cnt in db["blip_jun_new_tpl_phone"]:
    ph = phone.replace("@wa.gw.msging.net", "").replace("@wa.gw.ms", "").lstrip("+")
    if ph in jun_phones:
        jun_phones[ph][1] += cnt
    else:
        jun_phones[ph] = [ph, cnt, 0]

for tpl, phone, cnt in db["vox_jun_new_tpl_phone"]:
    ph = phone.lstrip("+")
    if ph in jun_phones:
        jun_phones[ph][1] += cnt
    else:
        jun_phones[ph] = [ph, cnt, 0]

# Add AC jun phones
for tpl, months in ac.get("tpl_month_phones", {}).items():
    for phone, cnt in months.get("jun", {}).items():
        ph = phone.replace("@wa.gw.msging.net", "").lstrip("+")
        if ph in jun_phones:
            jun_phones[ph][1] += cnt
        else:
            jun_phones[ph] = [ph, cnt, 0]

phone_data["jun"] = sorted(jun_phones.values(), key=lambda x: -x[1])

# Build jul phone data
jul_phones = {}
for tpl, phone, cnt in db["blip_jul_tpl_phone"]:
    ph = phone.replace("@wa.gw.msging.net", "").replace("@wa.gw.ms", "").lstrip("+")
    jul_phones[ph] = jul_phones.get(ph, 0) + cnt

for tpl, phone, cnt in db["vox_jul_tpl_phone"]:
    ph = phone.lstrip("+")
    jul_phones[ph] = jul_phones.get(ph, 0) + cnt

# Add AC jul phones
for tpl, months in ac.get("tpl_month_phones", {}).items():
    for phone, cnt in months.get("jul", {}).items():
        ph = phone.replace("@wa.gw.msging.net", "").lstrip("+")
        jul_phones[ph] = jul_phones.get(ph, 0) + cnt

phone_data["jul"] = sorted([[ph, cnt, 0] for ph, cnt in jul_phones.items()], key=lambda x: -x[1])

for m in MONTHS:
    month_data = phone_data.get(m, [])
    total_msgs = sum(row[1] for row in month_data)
    print(f"  {m}: {len(month_data):,} phones, {total_msgs:,} msgs")

with open("phone_inline.js", "w", encoding="utf-8") as f:
    f.write("const allPhoneData = " + json.dumps(phone_data, ensure_ascii=False) + ";")
print("  Written phone_inline.js")

# ============================================================
# 9. UPDATE template_phones.js (add jul)
# ============================================================
print("\n=== Updating template_phones.js ===")

with open("template_phones.js", "r", encoding="utf-8") as f:
    raw = f.read()
tpl_phones = json.loads(raw[len("const templatePhones = "):].rstrip().rstrip(";"))

# Add jun 24-30 phones to existing jun template_phones
jun_tpl = tpl_phones.get("jun", {})
for tpl, phone, cnt in db["blip_jun_new_tpl_phone"]:
    ph = phone.replace("@wa.gw.msging.net", "").replace("@wa.gw.ms", "").lstrip("+")
    if tpl not in jun_tpl:
        jun_tpl[tpl] = []
    # Find existing phone entry or add new
    found = False
    for entry in jun_tpl[tpl]:
        if entry[0] == ph:
            entry[1] += cnt
            found = True
            break
    if not found:
        jun_tpl[tpl].append([ph, cnt])

for tpl, phone, cnt in db["vox_jun_new_tpl_phone"]:
    ph = phone.lstrip("+")
    if tpl not in jun_tpl:
        jun_tpl[tpl] = []
    found = False
    for entry in jun_tpl[tpl]:
        if entry[0] == ph:
            entry[1] += cnt
            found = True
            break
    if not found:
        jun_tpl[tpl].append([ph, cnt])

tpl_phones["jun"] = jun_tpl

# Build jul template_phones
jul_tpl = defaultdict(lambda: defaultdict(int))
for tpl, phone, cnt in db["blip_jul_tpl_phone"]:
    ph = phone.replace("@wa.gw.msging.net", "").replace("@wa.gw.ms", "").lstrip("+")
    jul_tpl[tpl][ph] += cnt

for tpl, phone, cnt in db["vox_jul_tpl_phone"]:
    ph = phone.lstrip("+")
    jul_tpl[tpl][ph] += cnt

# Add AC jul phones
for tpl, months in ac.get("tpl_month_phones", {}).items():
    for phone, cnt in months.get("jul", {}).items():
        ph = phone.replace("@wa.gw.msging.net", "").lstrip("+")
        jul_tpl[tpl][ph] += cnt

tpl_phones["jul"] = {tpl: sorted([[ph, cnt] for ph, cnt in phones.items()], key=lambda x: -x[1])
                      for tpl, phones in jul_tpl.items()}

for m in MONTHS:
    print(f"  {m}: {len(tpl_phones.get(m, {}))} templates")

with open("template_phones.js", "w", encoding="utf-8") as f:
    f.write("const templatePhones = " + json.dumps(tpl_phones, ensure_ascii=False) + ";")
print("  Written template_phones.js")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("RESUMEN DE ACTUALIZACION")
print("=" * 60)
print(f"Periodo: Enero - Julio 7, 2026")
print(f"Templates totales: {len(new_data)}")
for m in MONTHS:
    idx = MONTH_IDX[m]
    total = sum(row[idx] for row in new_data)
    print(f"  {m}: {total:,} msgs")
print(f"\nArchivos actualizados:")
print(f"  - template_data.js")
print(f"  - template_totals.js")
print(f"  - phone_inline.js")
print(f"  - template_phones.js")
print(f"\nFalta actualizar manualmente:")
print(f"  - resumen.html (agregar julio, actualizar subtitulos)")
print(f"  - drivers-de-costo.html / index.html")
