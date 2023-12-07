import streamlit as st
import networkx as nx
import pandas as pd
import time
import asyncio
import json
import traceback
from streamlit_agraph import agraph, Node, Edge


class GraphConfig:
    def __init__(self, height, width):
        self.height = height
        self.width = width


def load_data():
    data = pd.read_csv('final_output.csv')
    return data


def load_graph_from_json(file_path):
    # Read the JSON from the file
    with open(file_path, 'r') as file:
        graph_json = json.load(file)

    # Convert the JSON to a graph
    return nx.node_link_graph(graph_json)


def perform_search(data, search_term):
    # Simple search logic: filter data based on search term in the selected category
    # Adjust this logic based on your actual data structure and search requirementsl
    try:
        data_list = []
        for col in data.columns.tolist():
            filtered_data = data.loc[data[col].str.contains(search_term, na=False) == True, :]
            data_list.append(filtered_data)

        final_data = pd.concat(data_list, axis = 0, sort = False).drop_duplicates()
        return final_data

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return pd.DataFrame()
    

def display_network_graph(graph):
    if('checkbox_fun_graph' not in st.session_state):
        st.text("it takes ~10 seconds to fully load")
        st.text("feel free to zoom in, or reload the page to actually get shit done with the search")
        # Load and preprocess data
        nodes = [Node(id=node, label=node) for node in graph.nodes()]
        edges = [Edge(source=edge[0], target=edge[1]) for edge in graph.edges()]

        config = GraphConfig(height=500, width=500)
        agraph(nodes=nodes, edges=edges, config=config)
        st.session_state['checkbox_fun_graph'] = True


def main():
    try:
        print('going again!')

        if('sidebar_exists' not in st.session_state):
            print('sidebar created!!')
            st.set_page_config(layout="wide")
            st.session_state['sidebar_exists'] = True
            st.session_state['data'] = load_data()
            st.session_state['graph'] = load_graph_from_json('graph_animation.json')
            st.session_state['written_report'] = ''

            st.session_state['youtube_links'] = 'no search performed yet'
            st.session_state['key_connections'] = 'no search performed yet'
            st.session_state['customer_persona'] = 'no search performed yet'
            st.session_state['practical_solution'] = 'no search performed yet'
            st.session_state['report_flag'] = False

            st.sidebar.title("welcome to synergy")

            st.sidebar.text('a search engine for ideas')
            st.sidebar.text('built on ~1000 buildspace ideas')
            st.sidebar.text('')

            st.header('outputs flow')
            st.write('if you are on mobile, you need to click the icon in top left of screen to open the search')

            list_ideas = [''] + st.session_state.data['title'].tolist()
            search_dropdown = st.sidebar.selectbox('select a result', options = list_ideas,
                                                    key = 'search_dropdown', on_change=main)

            checkbox_fun = st.checkbox('do you like fun but useless graphs? click the box to see one', key='checkbox_fun')
            

        if ('checkbox_fun' in st.session_state):
            if(st.session_state['checkbox_fun']):
                graph = load_graph_from_json('graph_animation.json')
                display_network_graph(graph)


        # if st.session_state['search_button']:
        if(st.session_state['search_dropdown'] != ''):
            # perform search and display results
            st.session_state['results'] = perform_search(data=st.session_state['data'], 
                                                        search_term=st.session_state['search_dropdown'])
        
            results = st.session_state['results']
            results_dropdown = results.loc[results['title'] == st.session_state['search_dropdown'], :]

            youtube_link_set = results_dropdown['link set'].tolist()[0]
            key_connections = results_dropdown['analysis'].tolist()[0].split('Key Connections and Recommendations:')[-1].split('Deep Dive Analysis:')[0]

            customer_persona = results_dropdown['analysis'].tolist()[0].split('Deep Dive Analysis:')[-1].split("- Customer Persona Development:")[-1].split("- Practical Solution Proposal:")[0]
            practical_solution = results_dropdown['analysis'].tolist()[0].split('- Practical Solution Proposal:')[-1]
            
            st.session_state['youtube_links'] = youtube_link_set
            st.session_state['key_connections'] = key_connections.lower()
            st.session_state['customer_persona'] = customer_persona.lower()
            st.session_state['practical_solution'] = practical_solution.lower()
            st.session_state['report_flag'] = True

        
        if(st.session_state['report_flag']):
            if(st.session_state['written_report'] == st.session_state['search_dropdown']):
                pass

            else:
                st.session_state['written_report'] = st.session_state['search_dropdown']
                st.session_state['report_flag'] = False
                st.sidebar.title("welcome to synergy")

                st.sidebar.text('a search engine for ideas')
                st.sidebar.text('built on ~1000 buildspace ideas')
                st.sidebar.text('')
                st.sidebar.text(f"loading {st.session_state['search_dropdown'].lower()}...")
                st.sidebar.text('')
                st.sidebar.text('first link is to original video')
                st.sidebar.text('other links are to collaborators')
                st.sidebar.text('reload the page to search again')
                st.header(f"{st.session_state['search_dropdown'].lower()} - youtube links")
                st.write(st.session_state['youtube_links'])
                st.text('')
                st.header(f"{st.session_state['search_dropdown'].lower()} - key connections")
                st.write(st.session_state['key_connections'])
                st.text('')
                st.header(f"{st.session_state['search_dropdown'].lower()} - customer personas")
                st.write(st.session_state['customer_persona'])
                st.text('')
                st.header(f"{st.session_state['search_dropdown'].lower()} - practical solution")
                st.write(st.session_state['practical_solution'])
                st.text('')
                st.text('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                st.text('')

                
    except Exception as e:
        print(e)
        print(traceback.format_exc())


if __name__ == "__main__":
    main()