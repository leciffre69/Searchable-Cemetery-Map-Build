import openpyxl, json, math

wb = openpyxl.load_workbook('data.xlsx')
ws = wb['Sheet1']

# Group records by plot
plots_data = {}
for row in ws.iter_rows(min_row=2, values_only=True):
    surname, forename, plot, dob, dod, age, notes = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
    if plot is None:
        continue
    key = str(plot).strip()
    if key not in plots_data:
        plots_data[key] = []
    plots_data[key].append({
        'surname': str(surname).strip() if surname else '',
        'forename': str(forename).strip() if forename else '',
        'dob': str(dob).strip() if dob else '',
        'dod': str(dod).strip() if dod else '',
        'age': str(age).strip() if age else '',
        'epitaph': str(notes).strip() if notes else ''
    })

# ---------------------------------------------------------------
# Grid layout: 14 plots per row (7 left + path + 7 right)
# Mirrors a typical churchyard with a central path
# ---------------------------------------------------------------

COLS = 15
CELL_W = 46
CELL_H = 28
PAD_X = 20
PAD_Y = 60

def plot_to_grid(n):
    left_per_row = 7
    right_per_row = 7
    per_row = left_per_row + right_per_row
    idx = n - 1
    row = idx // per_row
    pos_in_row = idx % per_row
    if pos_in_row < left_per_row:
        col = pos_in_row
    else:
        col = pos_in_row - left_per_row + 8
    return col, row

max_plot = 369
total_rows = math.ceil(max_plot / 14) + 1

SVG_W = PAD_X * 2 + COLS * CELL_W
SVG_H = PAD_Y * 2 + (total_rows + 3) * CELL_H + 80

def get_status(key):
    if key not in plots_data:
        return 'empty'
    occupants = plots_data[key]
    if not occupants:
        return 'empty'
    s = occupants[0]['surname'].lower()
    if '[not used]' in s:
        return 'unused'
    ep = occupants[0]['epitaph'].lower()
    if 'vacant' in ep or ('[vacant]' in ep):
        return 'vacant'
    if 'eroded' in ep or 'eroded' in s:
        return 'eroded'
    if not occupants[0]['surname'] and not occupants[0]['forename']:
        return 'empty'
    return 'occupied'

json_plots = []

for n in range(1, 370):
    key = str(n)
    col, row = plot_to_grid(n)
    x = PAD_X + col * CELL_W
    y = PAD_Y + row * CELL_H
    status = get_status(key)
    occupants = plots_data.get(key, [])
    json_plots.append({
        'plot': key,
        'cx': x + (CELL_W - 2) / 2,
        'cy': y + (CELL_H - 2) / 2,
        'x': x, 'y': y,
        'w': CELL_W - 2, 'h': CELL_H - 2,
        'status': status,
        'occupants': occupants
    })

# Special plots at bottom
special_keys = ['NK', '327A', '327B', '208B']
special_y = PAD_Y + (total_rows + 1) * CELL_H
for i, key in enumerate(special_keys):
    x = PAD_X + i * (CELL_W + 4)
    y = special_y
    occupants = plots_data.get(key, [])
    status = 'occupied' if occupants and (occupants[0]['surname'] or occupants[0]['forename']) else 'empty'
    json_plots.append({
        'plot': key,
        'cx': x + (CELL_W - 2) / 2,
        'cy': y + (CELL_H - 2) / 2,
        'x': x, 'y': y,
        'w': CELL_W - 2, 'h': CELL_H - 2,
        'status': status,
        'occupants': occupants
    })

with open('graveyard_plots.json', 'w', encoding='utf-8') as f:
    json.dump({
        'svgWidth': SVG_W,
        'svgHeight': SVG_H,
        'cellW': CELL_W,
        'cellH': CELL_H,
        'plots': json_plots
    }, f, ensure_ascii=False, indent=2)

print(f'Generated {len(json_plots)} plots')
print(f'SVG canvas: {SVG_W} x {SVG_H}')
