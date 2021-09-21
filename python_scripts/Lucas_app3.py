
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table 
import dash_cytoscape as cyto
import plotly.express as px
from plotly.graph_objects import *
import pandas as pd
from dash.dependencies import Input, Output, State
import json
import pickle
import jgraph as jg
import networkx as nx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial
from itertools import chain
import bellmanford as bf
import math
from dash.exceptions import PreventUpdate
import random

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})



styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


### Needed to update weights to be based on the full embedding, not the umap embeddings of the full embedding

#embeddings = pd.read_csv("../data/PheKnowLator_Instance_RelsOnly_NoOWL_node2vec_Embeddings_07Sept2020.emb",  skiprows = 1, sep = " " , index_col = 0, header = None)

umap_emb = pd.read_csv("umap_embeddings.csv", index_col = 0)

Graph = pd.read_csv("subGraph.csv", index_col = 0)

G = nx.read_gpickle('graph.gpickle')


umap_emb = umap_emb.set_index("index")
umap_emb["index"] = umap_emb.index


#filtered_identifiers.to_csv("../data/filtered_identifiers.csv")
ids = pd.read_csv("../data/filtered_identifiers.csv", index_col = 0)



# left = embeddings
# left = left.reindex(Graph["subject"])
# right = embeddings
# right = right.reindex(Graph["object"])

# left = left.to_numpy()
# right = right.to_numpy()

# weights = []
# for x in list(range(0, len(left),1)):
# 	print(x)
# 	tmp = 1 - spatial.distance.cosine(left[x],right[x])
# 	weights.append(tmp)



# Graph["weight"] = weights
# Graph["weight"] = abs(Graph["weight"])
# Graph["weight"] = 1- Graph["weight"]
# # # Graph["weight"] = (Graph["weight"]-min(Graph["weight"]))/(max(Graph["weight"]) - min(Graph["weight"]))


# Graph.to_csv("subGraph.csv")

# G = nx.from_pandas_edgelist(Graph, 'subject', 'object', edge_attr = "weight")
# G = G.to_undirected()
# nx.write_gpickle(G, 'graph.gpickle')

# degree = G.degree
# degrees = [val for (node, val) in G.degree()]
# inverse_centrality = degrees
# for x in inverse_centrality:
# 	inverse_centrality[x] = 1 - inverse_centrality[x]


# # nx.set_edge_attributes(G, degree, name = "degree")
# # #nx.write_edgelist(G, "Graph_nx", delimiter = ":")

# # #G = nx.read_edgelist(path = "Graph_nx", delimiter = ":")

centrality = nx.degree_centrality(G)
inverse_centrality = centrality
for x in inverse_centrality.keys():
	inverse_centrality[x] = 1 - inverse_centrality[x]

# # nx.set_edge_attributes(G, inverse_centrality, name = "inverse_centrality")


# print(nx.info(G))

# umap_emb[umap_emb["label"].str.contains("kynurenine")][["label","index"]]
# umap_emb[umap_emb["label"].str.contains("Alzh")][["label", "index"]]


# node1 = 203309
# node2 = 259395

# # # Graph[Graph["object"] == node2]

# nx.bidirectional_dijkstra(G, node1, node2, weight = "weight")

# bidirectional beam search


def bidirectional_beam_inverse_degree(node1, node2):
	path = [node2]
	nodes = nx.bfs_beam_edges(G, node1, inverse_centrality.get, width = 1000)
	while path[len(path)-1] != node1:
		for u,v in nodes:
			if v == node2:
				path.append(u)
				node2 = u
		nodes = nx.bfs_beam_edges(G, node1, inverse_centrality.get, width = 1000)
	return path 	


# bidirectional_beam_inverse_degree(node1, node2)


# ids[ids['0'] ==node1]['label']


node_degrees = nx.degree(G)

# node_degrees(node2)

# ### multiple pathway inputs
# umap_emb[umap_emb["label"].str.contains("neuroinf")][["label","index"]]
# umap_emb[umap_emb["label"].str.contains("oxidative stress")][["label","index"]]
# umap_emb[umap_emb["label"].str.contains("mitochondrial dysfunction")][["label","index"]]
# umap_emb[umap_emb["label"].str.contains("cholesterol metabolism")][["label","index"]]
# umap_emb[umap_emb["label"] =="autophagy"][["label","index"]]



# node1 = 88362 # neuroinflammation 
# node6 = 11319 # response to oxidative stress
# node3 = 367502 # mitochondrial dysfunction
# node4 =  75430 # abnormality of cholesterol metabolism
# node5 = 55866 # autophagy

# input_nodes = [node1, node6, node3, node4, node5]

# nodes = []
# for node in input_nodes:
# 	for u in nx.shortest_path(G,node, node2, weight = "weight" ):
# 		nodes.append(u)
# nodes = set(nodes)

# classes = list(umap_emb["class"].unique())

# null_map = {}
# n = 0
# for i in range(0,len(classes)):
# 	for j in range(i,len(classes)):
# 		null_map[n] = classes[i]+ " " + classes[j]
# 		n = n+1

# null_distributions_beam = []
# n = 0
# for i in range(0,len(classes)):
# 	rand_node1s = umap_emb[umap_emb["class"] == classes[i]]["index"]
# 	rand_node1s = rand_node1s[rand_node1s.isin(list(G.nodes))]
# 	for j in range(i, len(classes)):
# 		rand_node2s = umap_emb[umap_emb["class"] == classes[j]]["index"]
# 		rand_node2s = rand_node2s[rand_node2s.isin(list(G.nodes))]
# 		null = []
# 		nn = 0
# 		while(nn < 100):
# 			rand_node1 = rand_node1s.sample(n=1).item()
# 			rand_node2 = rand_node2s.sample(n=1).item()
# 			if rand_node1 in G and rand_node2 in G:
# 				if(nx.has_path(G, rand_node1, rand_node2)):
# 					tmp_nodes = bidirectional_beam_inverse_degree(rand_node1, rand_node2)
# 					null_degs = []
# 					for node in tmp_nodes:
# 						null_degs.append(node_degrees[node])
# 					tmp = sum(null_degs)
# 					null.append(tmp)
# 					nn = nn+1
# 					print(classes[i] + " "+ classes[j] + " " + str(nn))
# 		null_distributions_beam.append(null)



# null_distributions_vector = []
# n = 0
# for i in range(0,len(classes)):
# 	rand_node1s = umap_emb[umap_emb["class"] == classes[i]]["index"]
# 	rand_node1s = rand_node1s[rand_node1s.isin(list(G.nodes))]
# 	for j in range(i, len(classes)):
# 		rand_node1s = umap_emb[umap_emb["class"] == classes[j]]["index"]
# 		rand_node2s = rand_node2s[rand_node2s.isin(list(G.nodes))]
# 		null = []
# 		nn = 0
# 		while(nn < 100):
# 			rand_node1 = rand_node1s.sample(n=1).item()
# 			rand_node2 = rand_node2s.sample(n=1).item()
# 			if rand_node1 in G and rand_node2 in G:
# 				if(nx.has_path(G, rand_node1, rand_node2)):
# 					tmp = nx.bidirectional_dijkstra(G,rand_node1, rand_node2, weight = "weight")[0]
# 					null.append(tmp)
# 					nn = nn+1
# 					print(classes[i] + " "+ classes[j] + " " + str(nn))
# 		null_distributions_vector.append(null)



# pickle.dump(null_distributions_beam, open('null_distributions_beam', 'wb'))
# pickle.dump(null_distributions_vector, open('null_distributions_vector', 'wb'))




# set node coordinates
x,y,z = umap_emb["0"], umap_emb["1"], umap_emb["2"]

col = {"CHEBI": "blue" ,"HP": "red", "DOID": "yellow" ,"PR": "orange", "EFO" : "green", "SO": "purple", "GO":"brown"}
colors =  [col[key] for key in umap_emb["class"]]


trace1 = Scatter3d(
	name = "umap",
	x =x,
	y=y,
	z=z, 
	ids = umap_emb.index,
	mode = 'markers', 
	marker = dict(
		size = 1, 
		color = "grey", 
		opacity = 0.1	), 
	hoverinfo = "none" 
	)


trace2 = Scatter3d(
	name = "Selected Entity",
	x =pd.Series(x[1]),
	y=pd.Series(y[1]),
	z=pd.Series(z[1]), 
	mode = 'markers', 
	marker = dict(
		size = 1, 
		color = "grey", 
		opacity = 0.05	), 
	hoverinfo = "none" 
	)

node1 = 15558
nodes = [node1]
n = 1


newnodes1 = Graph[Graph['object'].isin(nodes)][["subject", "predicate"]]
newnodes2 = Graph[Graph['subject'].isin(nodes)][["object", "predicate"]]
newnodes = pd.concat([newnodes1["subject"],newnodes2["object"]])
newnodes = set(newnodes.tolist())
edge_vals = [1/n] * len(newnodes)
all_edge_vals = edge_vals
#edge_vals = np.where(edges.isin([12,27,173,260315]), np.asarray(edge_vals)/(n+.5), np.asarray(edge_vals)/(n+1)) 



while n < 2:
	nodes.extend(newnodes)
	n += 1
	newnodes1 = Graph[Graph['object'].isin(newnodes)][["subject", "predicate"]]
	newnodes2 = Graph[Graph['subject'].isin(newnodes)][["object", "predicate"]]
	newnodes = pd.concat([newnodes1["subject"],newnodes2["object"]])
	newnodes = set(newnodes.tolist())
	edge_vals = [1/n] * len(newnodes)
	all_edge_vals.extend(edge_vals)

subUmap = umap_emb[umap_emb["index"].isin(nodes) ]
subUmap = subUmap.set_index("index")
subUmap = subUmap.reindex(nodes)
xup,yup,zup = subUmap["0"],subUmap["1"],subUmap["2"]
weights = [x / 2 for x in all_edge_vals]


subUmap = umap_emb[umap_emb["index"].isin(nodes) ]
xup,yup,zup = subUmap["0"],subUmap["1"],subUmap["2"]


trace3 = Scatter3d(
		name = "Entity Graph",
		x =xup,
		y=yup,
		z=zup, 
		mode = "markers",
		marker = dict(
			size = 1, 
			color = "grey",
			opacity = .1 ),
		hoverinfo = "none"

			)
trace4 = Scatter3d(
		name = "Similar Nodes",
		x =xup,
		y=yup,
		z=zup, 
		mode = "markers",
		marker = dict(
			size = 1, 
			color = "grey",
			opacity = .1 ),
		hoverinfo = "none"

			)



fig = Figure(data=trace1)
fig.add_trace(trace2)
fig.add_trace(trace3)
fig.add_trace(trace4)

fig.update_layout(scene = dict(
                    xaxis_title='UMAP_1',
                    yaxis_title='UMAP_2',
                    zaxis_title='UMAP_3'))



### Listing the features to search for the dropdown menu
features = pd.melt(Graph[['subject','object']])
features = features["value"].unique()
labels = umap_emb[umap_emb["index"].isin(features)]
#labels = labels[labels["class"].isin("GO","HP","SO","EFO","DOID","PR")]
labels = labels[["index", "label"]]
tuples = [tuple(x) for x in labels.to_numpy()]

node_elements = [
	{
		'label': label, 'value' : id 
	}
	for id,label in tuples
	]


#### listing features for second dropdown
labels2 = umap_emb[umap_emb["index"].isin(features)]
#labels2 = labels2[labels2["class"].isin("GO","HP","SO","EFO","DOID","PR")]
labels2 = labels2[["index", "label"]]
tuples2 = [tuple(x) for x in labels2.to_numpy()]

node_elements2 = [
	{
		'label': label, 'value' : id 
	}
	for id,label in tuples2
	]




#### Laying out the dash app


app.layout = html.Div([
	html.Div([
		html.H1(children='UMAP embeddings'),

	   	html.Div(children='''
        	Choose source node.
    	'''),
    	  dcc.Dropdown(
		        id='dropdown',
		        options=node_elements
		  ),
			html.Div(children='''
        	Choose destination node.
    	'''),
    	  dcc.Dropdown(
		        id='dropdown2',
		        options=node_elements2
		  ),
	    dcc.Graph(
	    	id='3d_scat',
	    	figure=fig
	    	),
 #, style={'display': 'none'}))
	     
          #  html.Pre(id='input-data', style=styles['pre'])

	     ], style = {'width': '49%', 'float':'left'}),

	     html.Div([
		html.H1(children='Pathways'),
		html.Div(children='''
        	Choose Pathway Search Algorithm. 
    	'''),
		dcc.Dropdown(
		    id='pathway_search',
		    value='vector_weights',
		    clearable=False,
		    options=[
		        {'label': name, 'value': name}
		        for name in ['shortest_paths', 'node_degree', 'vector_weights']
		    ]
		),
		html.Div(children='''
        	Choose subgraph layout. 
    	'''),
    	dcc.Dropdown(
		    id='dropdown-update-layout',
		    value='grid',
		    clearable=False,
		    options=[
		        {'label': name.capitalize(), 'value': name}
		        for name in ['cose', 'random', 'circle', 'breadthfirst', 'concentric']
		    ]
		),
	    cyto.Cytoscape(
	        id='cytoscape',
	        layout={
	        	'name': 'concentric'},
	        style={'width': '100%', 'height': '400px'}
	                          
	        
	    )], style = {'width': '49%', 'float':'right'}),
])



# @app.callback(
#     Output('input-data', 'children'),
#     Input('dropdown', 'value'))
# def display_input_data(value):
# 	input_data = umap_emb[umap_emb["index"] == value].transpose()
# 	return '{}'.format(input_data)



# @app.callback(
#     Output('input-data2', 'children'),
#     Input('dropdown2', 'value'))
# def display_input_data(value):
# 	input_data = umap_emb[umap_emb["index"] == value].transpose()
# 	return '{}'.format(input_data)



@app.callback(Output('3d_scat', 'figure'),
			 Output('cytoscape', 'elements'),
			 Output('cytoscape', 'stylesheet'),
            [Input('dropdown', 'value'), 
            Input('dropdown2', 'value'),
            Input('pathway_search', 'value'),
            Input('3d_scat', 'clickData')
           ])
def chart_3d(source, destination,  search_type, clickData):
	if source is None:
		raise PreventUpdate
	else:

		global umap_emb
		#ctx = dash.callback_context
		#button_id = ctx.triggered[0]['prop_id'].split('.')[0]


		#if button_id != '3d_scat':
		x1= pd.Series(umap_emb[umap_emb["index"].isin([source, destination])]["0"])
		y1= pd.Series(umap_emb[umap_emb["index"].isin([source, destination])]["1"])
		z1= pd.Series(umap_emb[umap_emb["index"].isin([source, destination])]["2"])

		fig.update_traces(selector = dict(name = "Selected Entity"),
			x = x1,
			y = y1, 
			z = z1, 
			ids = umap_emb[umap_emb["index"] == source]['index'], 
			text = umap_emb[umap_emb["index"] == source]['label'],
			customdata = umap_emb[umap_emb["index"] == source]['IRI'],
			hovertemplate =  
			"<b>%{text}</b><br><br>" +
		    "IRI: %{customdata}<br>",
			marker = dict(
				size = 6, 
				color = "black"), 
			overwrite = True
			
			)

		node1 = source
		node2 = destination

		nodes = []

		if search_type == "shortest_paths":
			for u in nx.all_shortest_paths(G, node1, node2):
				nodes.append(u)
			flat_nodes = []
			for sublist in nodes:
			    for item in sublist:
			        flat_nodes.append(item)
			nodes = set(flat_nodes)
		elif search_type == "vector_weights":
			length, nodes = nx.bidirectional_dijkstra(G, node1,node2, weight = "weight")
		else:
			nodes = bidirectional_beam_inverse_degree(node1, node2)
				# degs = []
				# for node in nodes:
				# 	degs.append(node_degrees[node])
				# 	length = sum(degs)





		subUmap = umap_emb[umap_emb["index"].isin(nodes) ]
		xup,yup,zup = subUmap["0"],subUmap["1"],subUmap["2"]


		fig.update_traces(selector = dict(name = "Entity Graph"),
			x =xup,
			y=yup,
			z=zup, 
			ids = subUmap.index,
			text = subUmap['label'],
			customdata = subUmap["IRI"],
			mode = "markers",
			hovertemplate =  
			"<b>%{text}</b><br><br>" +
		    "IRI: %{customdata}<br>",
			marker = dict(
				size = 5, 
				color = "black",
				opacity = .5),
			overwrite = True		
		)

		subGraph = Graph[Graph['subject'].isin(nodes) & Graph['object'].isin(nodes)]
		features = pd.melt(subGraph[['subject','object']])
		features = features["value"].unique()
		labels = umap_emb[umap_emb["index"].isin(features)]
		labels = labels[["index", "label"]]
		tuples = [tuple(x) for x in labels.to_numpy()]

		node_elements = [
			{
				'data': {'id': id, 'label' : label }
			}
			for id,label in tuples
			]
		    

		edges = subGraph[["subject", "object"]]
		edges["edge_id"] = [ids.loc[ids['0'] == key]["label"].item() for key in subGraph["predicate"]]
		edge_tuples = [tuple(x) for x in edges.to_numpy()]
		edge_elements = [
			{'data': {'source': source, 'target':target, 'edge_id':edge_id}}
			for source, target, edge_id in edge_tuples
				
		]

		elements = node_elements + edge_elements
		edge_styles = [ids.loc[ids['0'] == key]["label"].item() for key in subGraph["predicate"]]

		stylesheet=[
			 {
		        'selector': 'node',
		        'style': {
		            'label': 'data(label)'
		        }

		    },
		    {
		        'selector': 'edge',
		        'style': {'label': 'data(edge_id)'}}
		       
		    
		    
		 ]


		# else: 
		clicknode = clickData['points'][0]['id']

		sub = umap_emb[umap_emb["index"] == clicknode][["0","1","2"]].to_numpy() - umap_emb[["0","1","2"]].to_numpy()
		distances = np.linalg.norm(sub, axis = 1)

		# distances = []
		# for x in umap_emb["index"]:
		# 	distance = np.linalg.norm(umap_emb[umap_emb["index"] == node2][["0","1","2"]].to_numpy() - umap_emb[umap_emb["index"] ==x][["0","1","2"]].to_numpy())
		# 	distances.append(distance)
		umap_emb["sim"] = distances
		umap_emb = umap_emb.sort_values(by = "sim", ascending = True)
		subUmap2 = umap_emb[1:11]
#subUmap2 = umap_emb[umap_emb["index"] == node2]

		x2,y2,z2 = subUmap2["0"],subUmap2["1"],subUmap2["2"]
		fig.update_traces(selector = dict(name = "Similar Nodes"),
			x =x2,
			y=y2,
			z=z2, 
			ids = subUmap2["index"],
			text = subUmap2['label'],
			customdata = subUmap2["IRI"],
			mode = "markers",
			hovertemplate =  
			"<b>%{text}</b><br><br>" +
		    "IRI: %{customdata}<br>",
			marker = dict(
				size = 5, 
				color = "purple", 
				opacity = .5, 
				line = dict(
					color = "black", 
					width = 1)),
			overwrite = True		
		)


	return fig, elements, stylesheet




# @app.callback(
#     Output('cytoscape', 'elements'),
#     Input('dropdown', 'value'), 
#     Input('dropdown2', 'value'),
#     Input('pathway_search', 'value'))
# def update_elements(source, destination, search_type):
# 	if source is None:
# 		raise PreventUpdate
# 	else:

# 		global umap_emb
# 		node1 = source
# 		node2 = destination

# 		nodes = []

# 		if search_type == "shortest_paths":
# 			for u in nx.all_shortest_paths(G, node1, node2):
# 				nodes.append(u)
				
# 			flat_nodes = []
# 			for sublist in nodes:
# 			    for item in sublist:
# 			        flat_nodes.append(item)

# 			nodes = set(flat_nodes)

# 		elif search_type == "vector_weights":
# 			length, nodes = nx.bidirectional_dijkstra(G, node1,node2, weight = "weight")

# 		else:
# 			nodes = bidirectional_beam_inverse_degree(node1, node2)


			
# 		subGraph = Graph[Graph['subject'].isin(nodes) & Graph['object'].isin(nodes)]



# 		features = pd.melt(subGraph[['subject','object']])
# 		features = features["value"].unique()
# 		labels = umap_emb[umap_emb["index"].isin(features)]
# 		labels = labels[["index", "label"]]
# 		tuples = [tuple(x) for x in labels.to_numpy()]

# 		node_elements = [
# 			{
# 				'data': {'id': id, 'label' : label }
# 			}
# 			for id,label in tuples
# 			]
		    

# 		edges = subGraph[["subject", "object"]]
# 		edge_tuples = [tuple(x) for x in edges.to_numpy()]
# 		edge_elements = [
# 			{'data': {'source': source, 'target':target}}
# 			for source, target in edge_tuples
				
# 		]

# 		elements = node_elements + edge_elements

# 		stylesheet=[
# 		    {
# 		        'selector': 'edge',
# 		        'style': {'label': ids.loc[ids['0'] == predicate]["label"].item()},
# 		        "text-wrap": "wrap"}
# 		        for predicate in subGraph["predicate"]
		    
		    
# 		 ]

# 		return elements


@app.callback(Output('cytoscape', 'layout'),
              Input('dropdown-update-layout', 'value'))
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }



if __name__ == '__main__':
    app.run_server(debug=True)


