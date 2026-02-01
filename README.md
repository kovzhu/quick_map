# 🗺️ quick-map

A pythonic, easy-to-use wrapper around `folium` designed to generate maps directly from Pandas DataFrames with minimal boilerplate.

## ✨ Features

- **Standardized Data Loading**: Automatically detects and renames common latitude/longitude column variations (`latitude`, `lat`, `long`, `x`, `y`, etc.).
- **Built-in Tile Layers**: Pre-configured with OpenStreetMap, Stamen Terrain, and CartoDB Positron.
- **Multiple Marker Types**: Support for both `CircleMarker` and standard `Marker` icons.
- **CCUS Specific Templates**: Specialized functions for CCUS (Carbon Capture, Utilization, and Storage) project analysis.
- **Jupyter Ready**: Works seamlessly in Jupyter Notebooks with `.show()`.

## 🚀 Quick Start

### 1. The Super Quick Way (Functional)
```python
import pandas as pd
import quick_map as qm

df = pd.read_csv("your_data.csv")
# Automatically finds lat/lon columns and shows the map
qm.quick_plot(df)
```

### 2. The Powerful Way (Object Oriented)
Use the default `map` instance for an interactive, stateful experience.

```python
from quick_map import map

# Add points with automatic cleaning
map.add_points(df, popup_cols=['name', 'capacity'], color='green')

# Add standard markers with icons
map.add_points(df, marker_type="marker", color="red", icon="info-sign")

map.show()
```

### 3. CCUS Specialized Analysis
If you are working with CCUS project data, use the built-in logic:

```python
import quick_map as qm

# Plots projects colored by maturity (Announced -> Operational)
qm.plot_ccus_maturity(df)

# Plots hubs vs single sources, planned vs deployed
qm.plot_ccus_status(df)
```

## 🛠️ Installation

```bash
# Using poetry
poetry add git+https://github.com/yourusername/quick_map.git
```

## 📖 API Reference

### `Map` Class
- `add_points(df, marker_type="circle", ...)`: Adds data to the map.
  - `marker_type`: `"circle"` or `"marker"`.
  - `popup_cols`: List of columns to show in the popup.
  - `icon`: Bootstrap icon name (for markers).
- `standardize_df(df)`: Helper to clean lat/lon columns.
- `save(path)`: Save map as HTML.
- `show()`: Display map in Jupyter.

## 🤝 Contributing
Contributions are welcome! Feel free to open issues or pull requests.
