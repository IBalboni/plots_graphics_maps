# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 21:10:06 2026
Plots from questionnaire data Penne amiche della scienza
 1. Plots of Italian provinces color coded by number of classes
 2. Plots of Italian provinced color coded by number of scientists
 3. Bubble plots with Countries of residence of scientist now
 4. Plot with doomain of research of the scientists
 
@author: ireba
"""

# %% [1] Import libraries and setup paths
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import matplotlib.colors as mcolors
import numpy as np



# Set the path to your file (using the one you provided)
# Note: Using r"" to handle backslashes in Windows paths

file_path = "C:/Users/ireba/mega/SciComm/penne/2025-26/sito scicomm/info_partecipanti_grafiche.xlsx" # Change extension to .csv if your file is a CSV

# %% [2] Load the data
# We'll try loading it as an Excel file first; if it's a CSV, use pd.read_csv
df = pd.read_excel(file_path)



# %% [3] Prepare Data for Both Maps


# --- 1. PROCESS SCHOOLS (With reduction for coloring) ---
col_schools = 'Provincia della scuola'
schools_counts = df[col_schools].str.strip().str.title().value_counts().reset_index()
schools_counts.columns = ['Provincia', 'Count_Raw']

# Identify top 2 and create the "Reduced" version for the map colors
top_2_idx = schools_counts['Count_Raw'].nlargest(2).index
schools_counts['Count_Reduced'] = schools_counts['Count_Raw'].copy()
schools_counts.loc[top_2_idx, 'Count_Reduced'] -= 10
schools_counts['Count_Reduced'] = schools_counts['Count_Reduced'].clip(lower=0)

# --- 2. PROCESS SCIENTISTS (Raw counts) ---
col_sci = 'Provenienza scienziati'
sci_counts = df[col_sci].str.strip().str.title().value_counts().reset_index()
sci_counts.columns = ['Provincia', 'Count_Sci']

# --- 3. LOAD MAP & MERGE ---
geojson_url = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_provinces.geojson"
italy_map = gpd.read_file(geojson_url)

# Merge Schools data
merged_map = italy_map.merge(schools_counts, left_on='prov_name', right_on='Provincia', how='left')
merged_map[['Count_Raw', 'Count_Reduced']] = merged_map[['Count_Raw', 'Count_Reduced']].fillna(0)

# Merge Scientists data
merged_sci = italy_map.merge(sci_counts, left_on='prov_name', right_on='Provincia', how='left')
merged_sci['Count_Sci'] = merged_sci['Count_Sci'].fillna(0)

print("Data processing complete. Variables 'merged_map' and 'merged_sci' are ready.")

# %% [4] Generate Schools Map (Balanced Colors + Original Scale Legend)


fig, ax = plt.subplots(1, 1, figsize=(10, 12))

# 1. Custom Blue Map
base_blues = plt.cm.Blues(np.linspace(0.2, 1, 256)) 
custom_blue_map = mcolors.ListedColormap(base_blues)

# 2. Background
merged_map.plot(ax=ax, color='#f8f8f8', edgecolor='#616161', linewidth=0.3)

# 3. Plot (Using Reduced counts for balance)
vibrant_schools = merged_map[merged_map['Count_Reduced'] > 0]
vibrant_schools.plot(
    column='Count_Reduced',
    cmap=custom_blue_map,
    linewidth=0.5,
    ax=ax,
    edgecolor='#616161'
)

# 4. Color Bar with Original Labels
max_red = merged_map['Count_Reduced'].max()
norm = mcolors.Normalize(vmin=0, vmax=max_red)
sm = plt.cm.ScalarMappable(cmap=custom_blue_map, norm=norm)

ticks = np.linspace(0, max_red, 5)
original_max = merged_map['Count_Raw'].max()
# Create labels: change the last tick to show the real max (38)
labels = [f"{int(t)}" for t in ticks[:-1]] + [f"{int(original_max)}"]

cbar = fig.colorbar(sm, ax=ax, shrink=0.5, pad=0.03)
cbar.set_ticks(ticks)
cbar.set_ticklabels(labels)
cbar.set_label('Numero di Classi', fontsize=12, fontweight='bold')

ax.set_title('Distribuzione Classi per Provincia', fontsize=18, fontweight='bold')
ax.axis('off')

plt.savefig('C:/Users/ireba/mega/SciComm/penne/2025-26/sito scicomm/mappa_scuole_finale.png', dpi=300, bbox_inches='tight')
plt.show()


#%% [5] scienziati provincie

# %% [6] Generate Scientists Map (Red #980000 + Color Bar)
fig, ax = plt.subplots(1, 1, figsize=(10, 12))

# 1. Custom Red Colormap
custom_red_map = mcolors.LinearSegmentedColormap.from_list("VibrantRed", ['#fce4ec', '#980000'])

# 2. Background
merged_sci.plot(ax=ax, color='#f8f8f8', edgecolor='#616161', linewidth=0.3)

# 3. Plot (Using raw Count)
vibrant_sci = merged_sci[merged_sci['Count_Sci'] > 0]
vibrant_sci.plot(
    column='Count_Sci',
    cmap=custom_red_map,
    linewidth=0.5,
    ax=ax,
    edgecolor='#616161'
)

# 4. Vertical Color Bar
norm_sci = mcolors.Normalize(vmin=0, vmax=merged_sci['Count_Sci'].max())
sm_sci = plt.cm.ScalarMappable(cmap=custom_red_map, norm=norm_sci)

cbar_sci = fig.colorbar(sm_sci, ax=ax, shrink=0.5, pad=0.03)
cbar_sci.set_label('Numero di Scienziati', fontsize=12, fontweight='bold', color='black')

ax.set_title('Provenienza degli Scienziati', fontsize=18, fontweight='bold', color='black')
ax.axis('off')

plt.savefig('C:/Users/ireba/mega/SciComm/penne/2025-26/sito scicomm/mappa_scienziati_finale_colorbar.png', dpi=300, bbox_inches='tight')
plt.show()
#%%
#########
#Luogo scienziati
##############


# %% [7] Bubble Chart: Yellow-Orange Theme & Label Mapping


# 1. Count and Clean
col_residenza = 'Residenza scienziati'
res_counts = df[col_residenza].str.strip().str.title().value_counts().reset_index()
res_counts.columns = ['Country', 'Count']

# 2. Filter out Italia and Map "Stati Uniti d'America" -> "Stati Uniti"
res_counts = res_counts[res_counts['Country'] != 'Italia'].reset_index(drop=True)
res_counts['Country'] = res_counts['Country'].replace({"Stati Uniti D’America": "Stati Uniti"})

# Sort by Count (Descending) to keep largest in the center
res_counts = res_counts.sort_values(by='Count', ascending=False).reset_index(drop=True)

# 3. Define Yellow-Orange Palette
# Using shades of #f4b629, #ff9400, and lighter golds
yellow_orange_palette = ['#ffd700', '#ffcc33', '#f4b629', '#ffb347', 
    '#ff9400', '#e69500', '#d14c00', '#b52600',]

# Calculate radii (max 26 -> radius ~0.18)
max_count = res_counts['Count'].max()
res_counts['radius'] = np.sqrt(res_counts['Count'] / max_count) * 0.18

# 4. Physics Simulation with Gravity
num_countries = len(res_counts)
center = np.array([0.5, 0.5])
pos = np.full((num_countries, 2), 0.5) + np.random.uniform(-0.02, 0.02, (num_countries, 2))

iterations = 1000
gravity = 0.05 

for _ in range(iterations):
    for i in range(num_countries):
        # A) Gravity: Pull bubble towards center
        vec_to_center = center - pos[i]
        pos[i] += vec_to_center * gravity
        
        # B) Collision: Push away from other bubbles
        for j in range(num_countries):
            if i == j: continue
            diff = pos[i] - pos[j]
            dist = np.linalg.norm(diff)
            min_dist = res_counts.loc[i, 'radius'] + res_counts.loc[j, 'radius'] + 0.005
            
            if dist < min_dist:
                if dist == 0: diff = np.array([0.01, 0.01]); dist = 0.014
                push = (diff / dist) * (min_dist - dist) * 0.5
                pos[i] += push

# 5. Plotting
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')

for i in range(num_countries):
    color = yellow_orange_palette[i % len(yellow_orange_palette)]
    radius = res_counts.loc[i, 'radius']
    
    # Draw Circle
    circle = plt.Circle((pos[i, 0], pos[i, 1]), radius, color=color, 
                        alpha=0.9, ec='white', lw=1.5, zorder=2)
    ax.add_patch(circle)
    
    # Optimized Text Scaling: 
    # Larger bubbles get bigger font, smaller bubbles get significantly smaller font
    # Base font is smaller now to prevent clutter on small dots
    f_size = 5 + (radius * 45) 
    
    ax.text(pos[i, 0], pos[i, 1], f"{res_counts.loc[i, 'Country']}\n{int(res_counts.loc[i, 'Count'])}", 
            ha='center', va='center', fontsize=f_size, fontweight='bold', color='black')

# 6. Final Styling
all_x = pos[:, 0]
all_y = pos[:, 1]
ax.set_xlim(all_x.min() - 0.2, all_x.max() + 0.2)
ax.set_ylim(all_y.min() - 0.2, all_y.max() + 0.2)
ax.axis('off')

# 7. Save
save_path = 'C:/Users/ireba/mega/SciComm/penne/2025-26/sito scicomm/bubble_chart_residenza_finale.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight', transparent=False)

plt.show()
#%%%%
#Ambito scienziati
####################


# %% [8] Process "Disciplina scienziati" (Donut Chart)
import colorsys
# 1. Count and Clean
col_disciplina = 'Disciplina scienziati'
disc_counts = df[col_disciplina].dropna().str.strip().str.capitalize().value_counts()
n_categories = len(disc_counts)

# 2. HIGH CONTRAST Sequence (Using your 6 anchor colors)
# We reorder them so that adjacent slices have the most different colors
high_contrast_base = ['#2f72b1', '#980000', '#40c69a', '#ff9400', '#33a6bf', '#f4b629']

# 3. Generate 22 Unique Colors (Variations in Lightness)
def adjust_lightness(color, amount=0.5):
    c = mcolors.to_rgb(color)
    h, l, s = colorsys.rgb_to_hls(*c)
    return colorsys.hls_to_rgb(h, max(0, min(1, l * amount)), s)

# Create sets of colors: Original, Lightened, and Darkened
all_distinct_colors = []
all_distinct_colors.extend(high_contrast_base) # 1-6: Original (High Contrast)
all_distinct_colors.extend([adjust_lightness(c, 1.4) for c in high_contrast_base]) # 7-12: Lightened
all_distinct_colors.extend([adjust_lightness(c, 0.7) for c in high_contrast_base]) # 13-18: Darkened
all_distinct_colors.extend([adjust_lightness(c, 1.7) for c in high_contrast_base]) # 19-24: Very Light

# Final list of 22 colors for the 22 categories
final_colors = all_distinct_colors[:n_categories]

# 4. Setup Plot
fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(aspect="equal"))

# 5. Filter percentages below 2.4%
def autopct_filter(pct):
    return ('%1.1f%%' % pct) if pct >= 2.4 else ''

wedges, texts, autotexts = ax.pie(
    disc_counts, 
    labels=None, 
    autopct=autopct_filter,
    startangle=140, 
    colors=final_colors,
    pctdistance=0.82,
    explode=[0.02] * n_categories, # Small visual gap
    textprops={'color':"white", 'weight':'bold', 'fontsize': 10}
)

# 6. Donut Hole
centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)

# 7. Central Text
total_scientists = disc_counts.sum()
ax.text(0, 0.12, 'TOTALE', ha='center', va='center', fontsize=16, fontweight='bold', color='#333333')
ax.text(0, -0.08, f'{total_scientists}', ha='center', va='center', fontsize=48, fontweight='bold', color='#980000')
ax.text(0, -0.22, 'Scienziati', ha='center', va='center', fontsize=12, color='#666666')

# 8. Legend
ax.legend(
    wedges, 
    [f"{label} ({count})" for label, count in zip(disc_counts.index, disc_counts.values)],
    title="Ambiti di Ricerca",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=10,
    frameon=False
)
ax.set_title('Ambiti di Ricerca dei nostri Scienziati', fontsize=22, fontweight='bold', pad=20)

plt.savefig('C:/Users/ireba/mega/SciComm/penne/2025-26/sito scicomm/donut_chart_discipline.png', dpi=300, bbox_inches='tight')

plt.show()
