import folium
import pandas as pd
import os
from datetime import datetime
from .core import Map


def planned_or_deployed(project_status):
    planned = ["Design", "Feasibility", "Announced", "Financing"]
    deployed = ["Operational", "Completed after operation", "Construction"]

    if project_status in planned:
        return "Planned"
    elif project_status in deployed:
        return "Deployed"
    else:
        return "Others"


def quick_plot(df, lat_col="lat", lon_col="lon", color="blue", save_path=None):
    """A quick function to plot a dataframe on a map."""
    m = Map()
    m.add_points(df, lat_col=lat_col, lon_col=lon_col, color=color)
    if save_path:
        m.save(save_path)
    return m.show()


def plot_ccus_status(df, output_path="maps"):
    """
    Recreates the 'map_by_deployed_or_planned' logic from CCUS analysis.
    """
    # 1. Filter and Prepare Data
    df = df.copy()
    if "size_category" in df.columns:
        df = df[df.size_category == "Large"]

    df["planned_or_deployed"] = df.status.apply(planned_or_deployed)
    df = df[df.status != "Others"]

    if "hub_development_flag" in df.columns:
        df["single_or_hub"] = df.hub_development_flag.apply(
            lambda x: "Hub" if x == True else "Single source"
        )
    else:
        df["single_or_hub"] = "Single source"

    df = df.dropna(subset=["lat", "lon"])

    # 2. Initialize Map
    m = Map()

    # 3. Define groups based on logic
    green = "#00AC4F"
    red = "#C84623"
    size = 2.5

    # Logic categories
    categories = [
        {
            "query": "(planned_or_deployed=='Planned') & (single_or_hub=='Hub')",
            "color": red,
            "fill": False,
            "label": "Hub, Planned",
        },
        {
            "query": "(planned_or_deployed=='Deployed') & (single_or_hub=='Hub')",
            "color": red,
            "fill": True,
            "label": "Hub, Deployed",
        },
        {
            "query": "(planned_or_deployed=='Deployed') & (single_or_hub=='Single source')",
            "color": green,
            "fill": True,
            "label": "Single, Deployed",
        },
        {
            "query": "(planned_or_deployed=='Planned') & (single_or_hub=='Single source')",
            "color": green,
            "fill": False,
            "label": "Single, Planned",
        },
    ]

    for cat in categories:
        group_df = df.query(cat["query"])
        group = folium.FeatureGroup(name=cat["label"])

        for _, row in group_df.iterrows():
            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=size,
                color=cat["color"],
                fill=cat["fill"],
                fill_color=cat["color"] if cat["fill"] else None,
                fill_opacity=1 if cat["fill"] else 0,
                weight=2,
                popup=folium.Popup(
                    f"Name: {row.get('name', 'N/A')}<br>Capacity: {row.get('capacity', 'N/A')}<br>{cat['label']}",
                    max_width=150,
                ),
            ).add_to(group)
        group.add_to(m.m)

    folium.LayerControl().add_to(m.m)

    if output_path:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        m.save(os.path.join(output_path, f"ccus_status_map_{ts}.html"))

    return m.show()


def plot_ccus_maturity(df, output_path="maps"):
    """
    Recreates the 'map_by_maturity' logic from CCUS analysis.
    """
    df = df.copy()
    # Filter as per original logic
    if "size_category" in df.columns:
        df = df[df["size_category"] == "Large"]
    if "dac_flag" in df.columns:
        df = df[df["dac_flag"] == False]

    df = df[df["status"] != "Completed after operation"]
    df = df.dropna(subset=["lat", "lon"])
    df = df[df["lat"] != 0]

    # Colors (S&P SPG_COLORS simplified or mocked if LISTS.SPG_COLORS is missing)
    spg_colors = ["#00A3E0", "#FFCD00", "#E03C31", "#007A33", "#6244BB", "#000000"]
    status_sequence = [
        "Announced",
        "Feasibility",
        "Design",
        "Financing",
        "Construction",
        "Operational",
    ]
    color_dict = {
        status: spg_colors[i % len(spg_colors)]
        for i, status in enumerate(status_sequence)
    }

    m = Map(location=[df.lat.mean(), df.lon.mean()] if not df.empty else [0, 0])

    for status in status_sequence:
        status_df = df[df["status"] == status]
        group = folium.FeatureGroup(name=status)
        for _, row in status_df.iterrows():
            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=5,
                color=color_dict.get(status, "gray"),
                fill=True,
                fill_opacity=0.7,
                popup=folium.Popup(
                    f"Name: {row.get('name')}<br>Status: {status}", max_width=150
                ),
            ).add_to(group)
        group.add_to(m.m)

    folium.LayerControl(collapsed=True).add_to(m.m)

    if output_path:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        m.save(os.path.join(output_path, f"ccus_maturity_map_{ts}.html"))

    return m.show()
