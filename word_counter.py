import sys
from datetime import datetime
import pandas as pd
import plotly.express as px
from collections import Counter
from pyvis.network import Network
import networkx as nx

####################################################################################################
# BRIEFING /----------------------------------------------------------------------------------------
# This application was created to count words in a text file, generate a dataframe with the information and present the data charts.
####################################################################################################

# Open the TXT file and get its text
def get_file_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "\nERROR: File Not Found!\n"
    except Exception as e:
        return f"\nERROR:\n{e}\n"


# Creates a dataframe with a dict of counted words
def create_dataframe(words_dict, csv_file_name=None):
    # Create a DataFrame from the dictionary
    df = pd.DataFrame(list(words_dict.items()), columns=['word', 'count'])
    df = df.sort_values(by="count")
    
    # If a filename is provided, export the DataFrame to a CSV file
    if csv_file_name:
        df.to_csv(f'{csv_file_name}.csv', index=False, encoding='utf-8-sig')
    return df


# Count how many times each word is repeated
def word_count(text):
    # Convert the string to lowercase to handle case insensitivity
    text = text.lower()
    
    # Split the string into words based on spaces
    words = text.split()
    
    # Use Counter to count the occurrences of each word
    word_counts = Counter(words)
    return dict(word_counts)


# Create a network graph using each line of a text file
def create_interactive_network_graph(file_path, output_html='network_graph.html'):
    # start the chart
    G = nx.Graph()

    # read the file line by line
    with open(file_path, 'r') as file:
        for line in file:
            words = line.strip().split()
            
            # connect the words
            if len(words) > 1:
                for i in range(len(words)):
                    for j in range(i + 1, len(words)):
                        G.add_edge(words[i], words[j])
    
    # check for nodes
    if G.number_of_nodes() > 0:
        # creates a instance of pyvis Network
        net = Network(notebook=False, cdn_resources='remote')

        # convert the graph from NetworkX to PyVis
        net.from_nx(G)
        
        # save
        net.write_html(f'{output_html}.html')
    else:
        print("\nERROR: Empty graph.\n")


# Run the app
def _main(path, network_graph=False):
    # get html data
    txt = get_file_text(path)

    # extract infos as a list
    words_dict = word_count(txt)

    # export file name
    timenow = str(datetime.now())[:19].replace(":", "-").replace(" ", "_")
    file_name = f'analysis\keyword_search_{timenow}'

    # create the dataframe
    df = create_dataframe(words_dict, file_name)
    print(f'\n{df}\n')

    # plot a network graph
    if network_graph:
        create_interactive_network_graph(path, output_html=file_name)


####################################################################################################
# INPUT ############################################################################################
####################################################################################################

_main("WORDS_INPUT.txt", network_graph=False)
