# 58 Tiles
# 232 edges
from ehtest.models import ehEdgePart, ehTile, ehExplorer


for i in range(58):
    newtile = None
    newtile = ehTile(special=False)
    newtile.save()
    for x in range(4):
        newedge = ehEdgePart(parent_tile=newtile, parent_cardinality=x)
        newedge.save()