import os
import folium
import pandas as pd
from datetime import datetime


class Map:
    """
    A class to generate maps from DataFrames using Folium.
    """

    def __init__(self, location=None, zoom_start=3, tiles="OpenStreetMap"):
        self.location = location
        self.zoom_start = zoom_start
        self.tiles = tiles
        self.m = folium.Map(
            location=self.location, zoom_start=self.zoom_start, tiles=self.tiles
        )
        self._add_default_tiles()

    def _add_default_tiles(self):
        """Adds a standard set of tile layers."""
        folium.TileLayer(
            tiles="Stamen Terrain",
            attr='&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
            name="Stamen Terrain",
        ).add_to(self.m)

        folium.TileLayer(
            tiles="https://tile.thunderforest.com/neighbourhood/{z}/{x}/{y}.png?apikey=734c0be502084e9cbc4ed238f91b0a3d",
            attr="Thunderforest",
            name="Thunderforest",
        ).add_to(self.m)

        folium.TileLayer(
            tiles="https://tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey=734c0be502084e9cbc4ed238f91b0a3d",
            attr="Thunderforest_trans",
            name="Thunderforest_trans",
        ).add_to(self.m)

        folium.TileLayer(
            tiles="https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoianZjMjY4OCIsImEiOiJja3Qwd2diczQwNGt1Mm9tbHJ1OWV5Y2hyIn0.Qwjn6ADRv_SSocKX9rEk6A",
            attr="Mapbox Satellite",
            name="Mapbox Satellite",
        ).add_to(self.m)

        folium.TileLayer("CartoDB Positron", attr="", name="CartoDB Positron").add_to(
            self.m
        )

    def standardize_df(self, df):
        """
        Renames common latitude and longitude column names to 'lat' and 'lon'.
        """
        rename_map = {}
        lat_aliases = ["latitude", "lat_col", "Latitude", "LAT", "y"]
        lon_aliases = ["longitude", "lon_col", "long", "Long", "Longitude", "LON", "x"]

        for col in df.columns:
            if col in lat_aliases:
                rename_map[col] = "lat"
            if col in lon_aliases:
                rename_map[col] = "lon"

        return df.rename(columns=rename_map)

    def add_points(
        self,
        df,
        lat_col=None,
        lon_col=None,
        popup_cols=None,
        marker_type="circle",  # "circle" or "marker"
        color="blue",
        radius=5,
        fill=True,
        weight=1,
        opacity=1,
        fill_opacity=0.7,
        icon=None,  # For standard markers
    ):
        """
        Add markers or circles to the map from a dataframe.
        """
        # Automatically try to standardize if lat/lon not provided
        work_df = self.standardize_df(df.copy())

        l_col = lat_col if lat_col else "lat"
        o_col = lon_col if lon_col else "lon"

        if l_col not in work_df.columns or o_col not in work_df.columns:
            print(f"Warning: Could not find columns {l_col} or {o_col} in dataframe.")
            return self

        df_clean = work_df.dropna(subset=[l_col, o_col])

        for _, row in df_clean.iterrows():
            popup_text = ""
            if popup_cols:
                popup_text = "<br>".join(
                    [f"{col}: {row[col]}" for col in popup_cols if col in row]
                )

            location = [row[l_col], row[o_col]]

            if marker_type == "marker":
                folium.Marker(
                    location=location,
                    popup=(
                        folium.Popup(popup_text, max_width=300) if popup_text else None
                    ),
                    icon=folium.Icon(color=color, icon=icon) if icon else None,
                ).add_to(self.m)
            else:
                folium.CircleMarker(
                    location=location,
                    radius=radius,
                    color=color,
                    fill=fill,
                    weight=weight,
                    opacity=opacity,
                    fill_opacity=fill_opacity,
                    popup=(
                        folium.Popup(popup_text, max_width=300) if popup_text else None
                    ),
                ).add_to(self.m)

        return self

    def save(self, file_path):
        """Save the map to an HTML file."""
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        self.m.save(file_path)
        print(f"Map saved to {file_path}")

    def show(self):
        """Return the map object (useful for Jupyter notebooks)."""
        return self.m
