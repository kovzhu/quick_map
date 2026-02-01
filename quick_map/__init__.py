from .core import Map
from .plotting import quick_plot, plot_ccus_status, plot_ccus_maturity

# Exporting a default Map instance as requested
# Note: Using 'map' as a variable name shadows the built-in map() function.
# If you run into issues, you can use 'from quick_map import Map' instead.
map = Map()

__all__ = ["Map", "map", "quick_plot", "plot_ccus_status", "plot_ccus_maturity"]
