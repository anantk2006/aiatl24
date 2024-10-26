from arcgis.gis import GIS
from arcgis.layers import MapFeatureLayer
from arcgis.geometry import Point
from arcgis.geometry.filters import intersects

gis = GIS()

one = gis.content.get("1311369dea53479ca9608cb5abca565f")
three = gis.content.get("365fa1f7f5314c0c81af516028f9c928")
map_feature_layer = MapFeatureLayer.fromitem(item = three)




query_extent = {
    "xmin": -11908433.363109391 - 1,
    "ymin": 5352150.796410866 - 1,
    "xmax": -11908433.363109391 + 1,
    "ymax": 5352150.796410866 + 1,
    "spatialReference": {"wkid": 102100},
}

query_filter = intersects(query_extent, sr=102100)

results = map_feature_layer.query(
    geometry_filter=query_filter, out_fields="*", as_df=False
)
for feature in results.features:
    print(feature.attributes)
print()

# print(results)
# m1 = gis.map("Miami, Florida")
# m1.content.add(three)
# display(m1)


