import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from textwrap import wrap

def create_tree_structure():
    tree_structure = {
        'Interest Income (TE)': {
            
            'Int Inc (TE) to Avg Earn Assets': {
                'Total Loan & Leases (TE)': {
                    'Real Estate': {},
                    'Commercial & Industrial': {},
                    'Individual': {},
                    'Agricultural': {}
                },
                'Total Investment Securities (TE)': {
                    'US Treas & Agency (Excl MBS)': {},
                    'Mortgage Backed Securities': {},
                    'All Other Securities': {}
                },
                'Interest-Bearing Bank Balances': {},
                'Federal Funds Sold & Resales': {}
            },
            'Avg Earning Assets to Avg Assets': {
                'Net Loans & Leases': {},
                'Interest-Bearing Bank Balances': {},
                'Federal Funds Sold & Resales': {},
                'Trading Account Assets': {},
                'Held-to-Maturity Securities': {},
                'Marketable Equity Sec at FV': {},
                'Available-for-Sale Securities': {}
            }
        },
        'Interest Expense': {}
    }
    return tree_structure

def add_data_to_tree_structure(tree_structure, data):
    for key in list(tree_structure.keys()):  # Iterate through a copy of the keys to avoid modification issues
        # Check if the current value is a dictionary
        if isinstance(tree_structure[key], dict):
            if key in data:
                bank_metric = data.get(f'{key}', 'N/A')
                peer_metric = data.get(f'{key} PG 2', 'N/A')
                percentile = data.get(f'{key} PCT', 'N/A')
                date = data.get('Date', 'N/A')
                node_data = f"{key}\nBank: {bank_metric}\nPeer: {peer_metric}\nPercentile: {percentile}\nDate: {date}"
                # Recursively call to add data to children
                add_data_to_tree_structure(tree_structure[key], data)
            else:
                node_data = key
            # Update the node with a dictionary containing the data and children
            tree_structure[key] = {'data': node_data, 'children': tree_structure[key]}
        else:
            print(f"Unexpected structure at {key}: {tree_structure[key]}")

def add_edges(G, parent, sub_tree):
    for child_key, child_value in sub_tree.items():
        if 'data' in child_value and 'children' in child_value:
            G.add_edge(parent, child_value['data'])
            add_edges(G, child_value['data'], child_value['children'])
        else:
            print(f"Malformed node at {child_key}: {child_value}")

def hierarchy_pos(G, root, width=3.0, vert_gap=0.5, xcenter=1, pos=None, parent=None, parsed=[]):
    if pos is None:
        pos = {root: (xcenter, 1)}
    else:
        pos[root] = (xcenter, pos[parent][1] - vert_gap)
    neighbors = list(G.neighbors(root))
    if parent in neighbors:
        neighbors.remove(parent)
    if len(neighbors) != 0:
        dx = width / len(neighbors)
        nextx = xcenter - width/2 - dx/2
        for child in neighbors:
            nextx += dx
            pos = hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, xcenter=nextx, pos=pos, parent=root)
    return pos

def draw_tree(tree_structure):
    G = nx.DiGraph()
    root_node = next(iter(tree_structure.values()))
    add_edges(G, root_node['data'], root_node['children'])

    pos = hierarchy_pos(G, root_node['data'])

    plt.figure(figsize=(15, 10))
    title = "Bank Data Visualization"
    plt.title(title, fontsize=20)

    for (u, v) in G.edges():
        points = [pos[u], ((pos[u][0]+pos[v][0])/2, pos[u][1]), ((pos[u][0]+pos[v][0])/2, pos[v][1]), pos[v]]
        plt.plot([point[0] for point in points], [point[1] for point in points], 'b-')

    for node, (x, y) in pos.items():
        wrapped_label = '\n'.join(wrap(node, width=20))
        plt.text(x, y, wrapped_label, ha='center', va='center', fontsize=7, fontweight='bold',
                 bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

    plt.gca().set_aspect('equal', adjustable='datalim')
    plt.axis('off')
    plt.tight_layout(pad=1.0)
    plt.show()

if __name__ == "__main__":
    excel_path = "C:/Users/kyleh/OneDrive/Documents/YouTube/UBPR/ubpr-report-generator/public/UBPR Example.xlsx"
    sheet_name = 'Structured UBPR Data'

    try:
        data = pd.read_excel(excel_path, sheet_name=sheet_name, engine='openpyxl').iloc[0].to_dict()
        tree_structure = create_tree_structure()
        add_data_to_tree_structure(tree_structure, data)
        draw_tree(tree_structure)
    except Exception as e:
        print(f"An error occurred: {e}")
