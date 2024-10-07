import json
from pyvis.network import Network

class KnowledgeGraph:
    def __init__(self, file_path):
        self.nodes = {}
        self.edges = {}
        self.load_data(file_path)
        
    def load_data(self, file_path):
        with open(file_path, 'r', encoding="utf8") as file:
            data = json.load(file)
            for entry in data:
                self.add_disease(entry)

    def add_disease(self, disease):
        disease_id = disease["id"]
        if disease_id not in self.nodes:
            self.nodes[disease_id] = disease
            self.edges[disease_id] = []
        
        
        for attribute in ["symptoms", "causes", "exams_and_tests", "treatment", "possible_complications", "alternate_names", "images", "related_medlineplus_health_topics"]:
            for item in disease.get(attribute, []):
                if item not in self.nodes:
                    self.nodes[item] = {}
                self.add_edge(disease_id, item, relation=attribute[:-1]) 

        for symptom in disease.get("symptoms", []):
            self.add_edge(disease_id, symptom, relation="has_symptom")

        for cause in disease.get("causes", []):
            self.add_edge(disease_id, cause, relation="has_cause")

        for test in disease.get("exams_and_tests", []):
            self.add_edge(disease_id, test, relation="requires_test")

        for treatment in disease.get("treatment", []):
            self.add_edge(disease_id, treatment, relation="has_treatment")

        for complication in disease.get("possible_complications", []):
            self.add_edge(disease_id, complication, relation="has_complication")

        for name in disease.get("alternate_names", []):
            self.add_edge(disease_id, name, relation="also_known_as")

        for image in disease.get("images", []):
            self.add_edge(disease_id, image, relation="has_image")

        for topic in disease.get("related_medlineplus_health_topics", []):
            self.add_edge(disease_id, topic, relation="related_to")
        
        # print(f"Edges for {disease_id}: {self.edges[disease_id]}")
            

            
    def normalize_attribute(self, items):
        # Assuming 'items' is a list of strings
        normalized_items = []
        for item in items:
            # Split by a delimiter if necessary, for example, a semicolon
            sub_items = item.split('; ')
            normalized_items.extend(sub_items)
        return normalized_items



    def add_edge(self, source, target, relation):
        if source not in self.edges:
            self.edges[source] = []
        if target not in self.nodes:
            self.nodes[target] = {}  # Ensure the target node is added
        self.edges[source].append((target, relation))



    def display_edges(self):
        for source, edge_list in self.edges.items():
            for target, relation in edge_list:
                print(f"({source}, {target}, {{'relation': '{relation}'}})")




    # Additional methods for ensuring this is a knowledge graph
    def find_shortest_path(self, source, target):
        if source not in self.nodes or target not in self.nodes:
            return None
        return self.find_paths(source, target, find_all=False)
    


    def find_all_paths(self, source, target):
        if source not in self.nodes or target not in self.nodes:
            return None
        return self.find_paths(source, target, find_all=True)
    


    def find_paths(self, source, target, find_all):
        if source not in self.edges:
            return None
        visited = {source}
        queue = [(source, [source])]

        paths = []
        while queue:
            current, path = queue.pop(0)
            if current == target:
                paths.append(path)
                if not find_all:
                    return paths
                continue
            for neighbor, _ in self.edges.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return paths if paths else None
    


    def find_neighbors(self, node):
        return [neighbor for neighbor, _ in self.edges.get(node, [])]
    

    
    def visualize(self):
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", notebook=True, cdn_resources='in_line')
        
        # Add nodes with labels
        for node, data in self.nodes.items():
            net.add_node(node, label=data.get('name', node), title=str(data), color="#f68c06")
        
        # Add edges with labels
        for source, edges in self.edges.items():
            for target, relation in edges:
                net.add_edge(source, target, title=relation, color="#848484")
        
        # Set options for a better layout and appearance
        options = """
        var options = {
        "nodes": {
            "borderWidth": 2,
            "borderWidthSelected": 4
        },
        "edges": {
            "color": {
            "inherit": true
            },
            "smooth": false
        },
        "interaction": {
            "navigationButtons": true,
            "keyboard": true
        },
        "physics": {
            "barnesHut": {
            "gravitationalConstant": -30000,
            "centralGravity": 0.3,
            "springLength": 95
            },
            "minVelocity": 0.75
        }
        }
        """
        net.set_options(options)
        
        # Write the HTML content directly to the file with utf-8 encoding
        html_content = net.generate_html()
        with open("kg_in_line.html", "w", encoding="utf8") as out:
            out.write(html_content)


    
    def query_knowledge_graph(self):
        print("What would you like to know about?")
        options = ["id", "name", "description", "alternate_names", "symptoms", "causes", "exams_and_tests", "treatment", "possible_complications", "images", "related_medlineplus_health_topics"]
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        selected_option_index = int(input("Enter the number of your choice: ")) - 1
        selected_option = options[selected_option_index]

        disease_name = input("Which disease are you referring to? ")

        # Initiate BFS to find the information
        result, traversal_order = kg.bfs_search(disease_name, selected_option)

        kg.visualize_bfs_traversed_path(traversal_order,result)

        if result:
            print(f"{selected_option.capitalize()}: {result}")
        else:
            print("Sorry, no information available for your selection.")



    def bfs_search(self, start_node_name, query):
        # Find the start node based on the given name
        start_node = None
        for node_id, node_data in self.nodes.items():
            if node_data.get('name', '').lower() == start_node_name.lower():
                start_node = node_id
                break

        if start_node is None:
            print(f"Start node not found for: {start_node_name}")
            return None, []

        visited = set()
        queue = [start_node]
        traversal_order = []

        while queue:
            current_node = queue.pop(0)
            traversal_order.append(current_node)

            print(f"Current Node: {current_node}, Neighbors: {self.edges[current_node]}")


            if current_node in visited:
                continue

            visited.add(current_node)
            # print(f"Visiting Node: {current_node}, Neighbors: {self.edges[current_node]}")
            
            neighbors = self.edges.get(current_node, [])
            
            # Print current node and its neighbors for debugging

            if query in self.nodes[current_node]:
                return self.nodes[current_node][query], traversal_order

            for neighbor, _ in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)

        return None, traversal_order  # Return None and the traversal order if the query is not found

        

    def visualize_bfs_traversed_path(self, traversal_order,result ,max_label_length=30):
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", notebook=True, cdn_resources="in_line")
        # Create the Central Node
        central_node_id = "Central Node"
        central_node_label = "Central Node"
        central_node_color = "red"  # Customize the color as needed

        # Increase the size of the central node
        central_node_size = 80  # You can adjust the size as needed

        net.add_node(
            central_node_id,
            label=central_node_label,
            color=central_node_color,
            size=central_node_size)

    
        # Keep track of nodes and edges added to the visualization
        added_nodes = set()
        added_edges = set()

        options = {
          "physics":{
              "barnesHut":{
                  "gravitationalConstant":-500000,
                  "centralGravity":12,
                  "springLength": 50,
                  "springConstant": 0.7,
                  "damping": 3,
                  "avoidOverlap": 10
              }
          },
          "interaction":{   
               "selectConnectedEdges": True

        }}

        net.options = options

        for node in traversal_order:
            node_label = self.nodes[node].get('name', node)
            # Truncate the label if it's longer than max_label_length
            if len(node_label) > max_label_length:
                node_label = node_label[:max_label_length] + '...'

            if node not in added_nodes:
                # Add the node to the network graph with the truncated label
                net.add_node(node, label=node_label, color='red', size=60)
                added_nodes.add(node)

            net.add_edge(central_node_id, node, color='white', width=8, length = 600)


            # Add edges for the current node if they are part of the BFS traversal
            for target, _ in self.edges.get(node, []):
                edge = (node, target)
                if edge not in added_edges:
                    # Add the target node if it hasn't been added yet
                    target_label = self.nodes[target].get('name', target)
                    if len(target_label) > max_label_length:
                        target_label = target_label[:max_label_length] + '...'

                    if target not in added_nodes:
                        if target not in result:
                            net.add_node(target, label=target_label, color='blue')
                            added_nodes.add(target)
                            net.add_edge(node, target, color='green', width=2, node_opacity=0.1)

                        else:
                            net.add_node(target, label=target_label, color='red')
                            added_nodes.add(target)
                            net.add_edge(node, target, color='white', width=8, node_opacity=4)
                    # Add the edge between the current node and the target node
                    added_edges.add(edge)

        # Write the HTML content
        html_content = net.generate_html()
        with open("bfs_traversed_only.html", "w", encoding="utf8") as out:
            out.write(html_content)


            


# build small graph and visualize - after runnning open kg_in_line.html file in chrome or edge browser
# filepath = 'data/sample.json'
# kg = KnowledgeGraph(filepath)
# kg.visualize()



# Build the entire graph and test
filepath = 'data/disease_cleaned.json'
kg = KnowledgeGraph(filepath)
kg.query_knowledge_graph()
