import networkx
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd

#place_name = input("Enter a city or address(press Enter for Las Vegas: NM): ").strip()
#if not place_name:

place_name = "Las Vegas, NM"

G = ox.graph_from_place(place_name)
tags = {"leisure": "park", "amenity":["library", "cafe","restaurant", "fast_food", "ice_cream"]}
gdf = ox.features.features_from_place(place_name, tags)
#ox.plot_footprints(gdf)

df_amenities = gpd.GeoDataFrame({
    'name': gdf['name'],
    'coord':gdf.geometry.apply(lambda x: x.centroid)
}).dropna()

nodes_amen = {}
for _, row in df_amenities.iterrows():
    nearest_node = ox.distance.nearest_nodes(G, row['coord'].x, row['coord'].y)
    nodes_amen[nearest_node] = row['name']
nx.set_node_attributes(G, nodes_amen, name="loc_name")

amenity_nodes = list(nodes_amen.keys())
origin = amenity_nodes[0]

for node in amenity_nodes[1:]:
    try:
        nx.shortest_path(G, source=origin, target=node)
    except nx.NetworkXNoPath:
        connect_path = nx.shortest_path(G.to_undirected(), source=origin, target=node)
        for u, v in zip(connect_path[:-1], connect_path[1:]):
            if not G.has_edge(u, v):
                G.add_edge(u, v)
            if not G.has_edge(v, u):
                G.add_edge(v, u)

fig, ax = plt.subplots(figsize=(8,8))
ox.plot_graph(G, ax=ax, node_color="lightgray", edge_color="lightgray", show=False, close=False)
node_positions = {n:(G.nodes[n]["x"],G.nodes[n]["y"]) for n in nodes_amen}
nx.draw_networkx_nodes(G, pos=node_positions, nodelist=nodes_amen.keys(), node_size=50,node_color="red")
for node, name in nodes_amen.items():
    x,y = G.nodes[node]["x"], G.nodes[node]["y"]
    plt.text(x,y, name, fontsize=8, ha="right", va="bottom", color="black")


origin = list(nodes_amen.keys())[0]
dest = list(nodes_amen.keys())[20]
path = nx.shortest_path(G, source=origin, target=dest)
#dest = amenity_nodes[20]
#path = nx.shortest_path(G, source=origin, target=dest)
ox.plot_graph_route(G, path, show=False, close=False)



plt.show()
fig.savefig("map.png")

#nod_ids = list(G.nodes())
#print(node_ids)
#for n in nod_ids:
#    print(G.nodes[n])

#plt.figure(figsize=(10,10))
#plt.scatter(df_amenities["coord"].x, df_amenities["coord"].y)

#for_,row in df_amenities.iterrows():
#plt.text(row['coord'].x, row['coord'].y, row['name'])
#plt.show()

#nodes, edges = ox.graph_to_gdfs(G)
#min_lon, max_lon = nodes['x'].min(),nodes['x'].max()
#min_lat, max_lat = nodes['y'].min(),nodes['y'].max()
#center_lon = (min_lon+max_lon)/2
#origin_node = ox.distance.nearest_nodes(G, min_lon, min_lat)
#destination_node = ox.distance.nearest_nodes(G, max_lon, max_lat)

#try:
#    route = nx.shortest_path(G, origin_node, destination_node)
#    fig,ax = ox.plot_graph_route(G, route)
#except networkx.NetworkXException:
#    print("No route found")
#    fig,ax = ox.plot_graph(G)

