#!/usr/bin/env python
# coding: utf-8

# ## Module 3 Assignment - Building RAG systems with a Vector Database
# 
# ---
# 
# In this assignment you will work with [Weaviate API](https://weaviate.io/) to build a tiny RAG system. You will:
# 
# - Load a [collection](https://weaviate.io/developers/weaviate/manage-data/collections) for BBC News data.
# - Use the Weaviate API to retrieve documents from the vector database.
# - Create functions to retrieve data based on Semantic Search, BM25 and Hybrid Search (using RRF) using the Weaviate API.
# - Use an LLM to generate responses.
# 
# **IMPORTANT**: This assignment assumes you know how to handle simple tasks with collections in the Weaviate API. If you are not familiar with it yet, please read the Ungraded Lab on the Weaviate API! Furthermore, the data you will be working here is already *chunked*. You can get more hands-on experience on chunking reading the Ungraded Lab on chunking!

# 
# # Table of Contents
# - [ 1 - Loading the libraries](#1)
# - [ 2 - Setting up the Weaviate Client and loading the data](#2)
#   - [ 2.1 Loading the Weaviate Client](#2-1)
#   - [ 2.2 Loading the data](#2-2)
# - [ 3 - Loading the Collection](#3)
#   - [ 3.1 Metadata filtering](#3-1)
#     - [ Exercise 1](#ex01)
#   - [ 3.2 Semantic search](#3-2)
#     - [ Exercise 2](#ex02)
#   - [ 3.3 BM25 Serach](#3-3)
#     - [ Exercise 3](#ex03)
#   - [ 3.4 Hybrid search](#3-4)
#     - [ Exercise 4](#ex04)
#     - [ Exercise 5](#ex05)
# - [ 4 - Incorporating the Weaviate API into our previous schema](#4)
#   - [ 4.1 Generating the final prompt](#4-1)
#   - [ 4.2 LLM call](#4-2)
# - [ 5 - Experimenting with Your RAG System](#5)
# 

# ---
# <h4 style="color:black; font-weight:bold;">USING THE TABLE OF CONTENTS</h4>
# 
# JupyterLab provides an easy way for you to navigate through your assignment. It's located under the Table of Contents tab, found in the left panel, as shown in the picture below.
# 
# ![TOC Location](images/toc.png)
# 
# ---
# 
# <h4 style="color:green; font-weight:bold;">TIPS FOR SUCCESSFUL GRADING OF YOUR ASSIGNMENT:</h4>
# 
# - All cells are frozen except for the ones where you need to submit your solutions or when explicitly mentioned you can interact with it.
# 
# - You can add new cells to experiment but these will be omitted by the grader, so don't rely on newly created cells to host your solution code, use the provided places for this.
# 
# - Avoid using global variables unless you absolutely have to. The grader tests your code in an isolated environment without running all cells from the top. As a result, global variables may be unavailable when scoring your submission. Global variables that are meant to be used will be defined in UPPERCASE.
# 
# - - To submit your notebook for grading, first save it by clicking the 💾 icon on the top left of the page and then click on the <span style="background-color: blue; color: white; padding: 3px 5px; font-size: 16px; border-radius: 5px;">Submit assignment</span> button on the top right of the page.
# ---

# <a id='1'></a>
# ## 1 - Loading the libraries
# 
# ---
# 
# Run the cell below to load the necessary libraries for this assignment.

# In[ ]:


import joblib
import weaviate
from weaviate.classes.query import (
    Filter, 
    Rerank
)


# In[ ]:


import flask_app
import weaviate_server
from utils import (
    generate_with_single_input,
    print_object_properties,
    display_widget
)
import unittests


# <a id='2'></a>
# ## 2 - Setting up the Weaviate Client and loading the data
# 
# ---
# 
# In this section, you will set up the Weaviate client and load the data, which consists of the [BBC news dataset](https://www.kaggle.com/datasets/gpreda/bbc-news) adapted from Kaggle.

# <a id='2-1'></a>
# ### 2.1 Loading the Weaviate Client
# 
# Let's connect the Weaviate client to begin working with the Weaviate API. The server is already running on the backend. 
# 
# **Troubleshooting:**
# 
# - If you encounter issues loading the next cell, try restarting your kernel, clicking in the circled arrow in the panel above.

# In[ ]:


client = weaviate.connect_to_local(port=8079, grpc_port=50050)


# <a id='2-2'></a>
# ### 2.2 Loading the data
# 
# Now, let's load the data. The dataset is structured with the following fields:
# 
# - **`title`**: The headline of the article.
# - **`pubDate`**: The publication date and time of the article.
# - **`guid`**: A unique identifier for the article, commonly used for listing.
# - **`link`**: A URL link to access the full article online.
# - **`description`**: A brief summary or teaser of the article's content.
# - **`article_content`**: The complete text of the article, providing detailed information.

# In[ ]:


bbc_data = joblib.load('data/bbc_data.joblib')


# In[ ]:


print_object_properties(bbc_data[0])


# <a id='3'></a>
# ## 3 - Loading the Collection
# 
# ---
# 
# In this section, you will load the collection containing the BBC News dataset.

# In[ ]:


collection = client.collections.get("bbc_collection")


# In[ ]:


print(f"The number of elements in the collection is: {len(collection)}")


# Let's fetch one example of object in this collection.

# In[ ]:


object = collection.query.fetch_objects(limit = 1, include_vector = True).objects[0]
print("Printing the properties (some will be truncated due to size)")
print_object_properties(object.properties)
print("Vector: (truncated)",object.vector['main_vector'][0:15])
print("Vector length: ", len(object.vector['main_vector']))


# The vector length is `768`. So every chunk in the vector database is mapped into a 768 dimension vector. This is the vector the Weaviate API uses to perform semantic search.

# <a id='ex01'></a>
# 
# <a id='3-1'></a>
# ### 3.1 Metadata filtering
# 
# <a id='ex01'></a>
# ### Exercise 1
# 
# In this exercise, you will implement a metadata filtering function. This function will take several inputs: a property (such as `article_content`, `title`, `pubDate`, etc.), the values you want to filter by, the collection you want to search in, and the number of items you want to retrieve.
# 
# <details>
# <summary style="color: green;">Hint 1</summary>
# <p>Remember that to perform filtering based only on metadata, the appropriate method to use is <code>collection.query.fetch_objects</code>.</p>
# </details>
# <details>
# <summary style="color: green;">Hint 2</summary>
# <p>When using <code>collection.query.fetch_objects</code>, you must provide the <code>metadata_property</code> as the <code>property</code> and the corresponding <code>Filter</code> object.</p>
# </details>
# <details>
# <summary style="color: green;">Hint 3</summary>
# <p>The filter object should be used with the method <code>.by_property</code> for the appropriate property, and <code>.contains_any</code> with the relevant values. A typical call would be <code>Filter.by_property(metadata_property).contains_any(values)</code>.</p>
# <p>To limit the results, use <code>limit=limit</code> within the <code>.fetch_objects</code> method.</p>
# </details>

# In[ ]:


# GRADED CELL 

def filter_by_metadata(metadata_property: str, 
                       values: list[str], 
                       collection: "weaviate.collections.collection.sync.Collection" , 
                       limit: int = 5) -> list:
    """
    Retrieves objects from a specified collection based on metadata filtering criteria.

    This function queries a collection within the specified client to fetch objects that match 
    certain metadata criteria. It uses a filter to find objects whose specified 'property' contains 
    any of the given 'values'. The number of objects retrieved is limited by the 'limit' parameter.

    Args:
    metadata_property (str): The name of the metadata property to filter on.
    values (List[str]): A list of values to be matched against the specified property.
    collection_name (weaviate.collections.collection.sync.Collection): The collection to query.
    limit (int, optional): The maximum number of objects to retrieve. Defaults to 5.

    Returns:
    List[Object]: A list of objects from the collection that match the filtering criteria.
    """
    ### START CODE HERE ###

    # Retrieve using collection.query.fetch_objects

    response = None

    ### END CODE HERE ###

    response_objects = [x.properties for x in response.objects]

    return response_objects


# In[ ]:


# Let's get an example
res = filter_by_metadata('title', ['Taylor Swift'], collection, limit = 2)
for x in res:
    print_object_properties(x)


# **Expected output**
# ```
# article_content: The 2024 awards season kicked off in style at the Golden Globes - the first major red carpet event o...(truncated)
# chunk: some of his previous get-ups. The Bear's Jeremy Allen White - who recently became the new face (and ...(truncated)
# chunk_index: 4
# description: Stars including Margot Robbie and Taylor Swift arrived in a variety of eye-catching outfits.
# link: https://www.bbc.co.uk/news/entertainment-arts-67908727?at_medium=RSS&at_campaign=KARANGA
# pubDate: 2024-01-08 03:23:58+00:00
# title: Margot Robbie, Taylor Swift and more on Golden Globes red carpet
# 
# article_content: The 2024 awards season kicked off in style at the Golden Globes - the first major red carpet event o...(truncated)
# chunk: headpiece - not entirely a fashion choice. She says the "protective veil" is because she hurt her fa...(truncated)
# chunk_index: 5
# description: Stars including Margot Robbie and Taylor Swift arrived in a variety of eye-catching outfits.
# link: https://www.bbc.co.uk/news/entertainment-arts-67908727?at_medium=RSS&at_campaign=KARANGA
# pubDate: 2024-01-08 03:23:58+00:00
# title: Margot Robbie, Taylor Swift and more on Golden Globes red carpet
# ```

# In[ ]:


# Test your solution!
unittests.test_filter_by_metadata(filter_by_metadata, client)


# <a id='ex02'></a>
# 
# <a id='3-2'></a>
# ### 3.2 Semantic search
# 
# <a id='ex02'></a>
# ### Exercise 2
# 
# In this exercise, you will implement a semantic search retrieval, similar to the one you created in the previous assignment, but this time utilizing the Weaviate API.
# 
# <details>
# <summary style="color: green;">Hint</summary>
# <p>Remember that to perform semantic search, you should use the method <code>collection.query.near_text</code>.</p>
# <p>The <code>top_k</code> parameter in the function dictates how many results to retrieve. In Weaviate, this is referred to as <code>limit</code>. Adjust this parameter as needed.</p>
# </details>

# In[ ]:


# GRADED CELL 

def semantic_search_retrieve(query: str,
                             collection: "weaviate.collections.collection.sync.Collection" , 
                             top_k: int = 5) -> list:
    """
    Performs a semantic search on a collection and retrieves the top relevant chunks.

    This function executes a semantic search query on a specified collection to find text chunks 
    that are most relevant to the input 'query'. The search retrieves a limited number of top 
    matching objects, as specified by 'top_k'. The function returns the 'chunk' property of 
    each of the top matching objects.

    Args:
    query (str): The search query used to find relevant text chunks.
    collection (weaviate.collections.collection.sync.Collection): The collection in which the semantic search is performed.
    top_k (int, optional): The number of top relevant objects to retrieve. Defaults to 5.

    Returns:
    List[str]: A list of text chunks that are most relevant to the given query.
    """
    ### START CODE HERE ###

    # Retrieve using collection.query.near_text
    response = None

    ### END CODE HERE ###

    response_objects = [x.properties for x in response.objects]

    return response_objects


# In[ ]:


# Let's have an example!
print_object_properties(semantic_search_retrieve(query = 'Tell me about the last Taylor Swift show', collection = collection, top_k = 2))


# **Expected Output**
# ```
# article_content: Taylor Swift has finished the European leg of her Eras Tour with a record-breaking show at Wembley S...(truncated)
# chunk: size crowd at all". At an earlier show in Liverpool, she had also called the Eras Tour the “most exh...(truncated)
# chunk_index: 10
# description: The star is joined by Florence + The Machine and sings So Long, London at her final UK show.
# link: https://www.bbc.com/news/articles/cr5nr3n6epvo
# pubDate: 2024-08-21 03:02:08+00:00
# title: 'I've never had it this good' - Taylor Swift thanks fans after new Wembley record
# 
# article_content: Taylor Swift has finished the European leg of her Eras Tour with a record-breaking show at Wembley S...(truncated)
# chunk: regular part of the setlist. Last week, the star was joined by Ed Sheeran to play the songs Endgame ...(truncated)
# chunk_index: 4
# description: The star is joined by Florence + The Machine and sings So Long, London at her final UK show.
# link: https://www.bbc.com/news/articles/cr5nr3n6epvo
# pubDate: 2024-08-21 03:02:08+00:00
# title: 'I've never had it this good' - Taylor Swift thanks fans after new Wembley record
# 
# ```

# In[ ]:


unittests.test_semantic_search_retrieve(semantic_search_retrieve, client)


# <a id='ex03'></a>
# 
# <a id='3-3'></a>
# ### 3.3 BM25 Serach
# 
# <a id='ex03'></a>
# ### Exercise 3
# 
# In this exercise, you will implement a BM25 retrieval, similar to the one you created in the previous assignment, but now using the Weaviate API.
# <details>
# <summary style="color: green;">Hint</summary>
# <p>To perform a BM25 search, use the method <code>collection.query.bm25</code>.</p>
# <p>The <code>top_k</code> parameter in the function specifies how many results to retrieve. In Weaviate, this parameter is referred to as <code>limit</code>. Adjust this accordingly.</p>
# </details>

# In[ ]:


# GRADED CELL 

def bm25_retrieve(query: str, 
                  collection: "weaviate.collections.collection.sync.Collection" , 
                  top_k: int = 5) -> list:
    """
    Performs a BM25 search on a collection and retrieves the top relevant chunks.

    This function executes a BM25-based search query on a specified collection to identify text 
    chunks that are most relevant to the provided 'query'. It retrieves a limited number of the 
    top matching objects, as specified by 'top_k', and returns the 'chunk' property of these objects.

    Args:
    query (str): The search query used to find relevant text chunks.
    collection (weaviate.collections.collection.sync.Collection): The collection in which the BM25 search is performed.
    top_k (int, optional): The number of top relevant objects to retrieve. Defaults to 5.

    Returns:
    List[str]: A list of text chunks that are most relevant to the given query.
    """

    ### START CODE HERE ###

    # Retrieve using collection.query.bm25
    response = None

    ### END CODE HERE ### 

    response_objects = [x.properties for x in response.objects]
    return response_objects 


# In[ ]:


print_object_properties(bm25_retrieve('Tell me about the last Taylor Swift show', collection, top_k = 2))


# **Expected Output**
# ```
# article_content: Rapper Killer Mike won three Grammys in the rap category - best rap song, best rap performance and b...(truncated)
# chunk: police brutality and systemic racism. He was a highly visible supporter of Bernie Sanders' two campa...(truncated)
# chunk_index: 4
# description: The 48-year-old was detained on a misdemeanour charge after winning three awards in the rap category.
# link: https://www.bbc.co.uk/news/world-us-canada-68201021?at_medium=RSS&at_campaign=KARANGA
# pubDate: 2024-02-05 23:27:08+00:00
# title: Killer Mike dismisses arrest at Grammys as 'speed bump'
# 
# article_content: Rapper Killer Mike won three Grammys in the rap category - best rap song, best rap performance and b...(truncated)
# chunk: Nicki Minaj. He also won a third award for best rap album with his album Michael. "You cannot tell m...(truncated)
# chunk_index: 3
# description: The 48-year-old was detained on a misdemeanour charge after winning three awards in the rap category.
# link: https://www.bbc.co.uk/news/world-us-canada-68201021?at_medium=RSS&at_campaign=KARANGA
# pubDate: 2024-02-05 23:27:08+00:00
# title: Killer Mike dismisses arrest at Grammys as 'speed bump'
# ```

# In[ ]:


unittests.test_bm25_retrieve(bm25_retrieve, client)


# <a id='ex04'></a>
# 
# <a id='3-4'></a>
# ### 3.4 Hybrid search
# 
# <a id='ex04'></a>
# ### Exercise 4
# 
# In this exercise, you will implement a Reciprocal Rank Fusion (RRF) retrieval system using the Weaviate API. To achieve this, you will need to use the `collection.query.hybrid` method.
# 
# 
# 
# <details>
# <summary style="color: green;">Hint</summary>
# <p>To perform a hybrid search, use the method <code>collection.query.hybrid</code>.</p>
# <p>The <code>top_k</code> parameter in the function specifies how many results to retrieve. In Weaviate, this is referred to as <code>limit</code>. Make sure to also include the <code>alpha</code>.</p>
# </details>

# In[ ]:


# GRADED CELL 

def hybrid_retrieve(query: str, 
                    collection: "weaviate.collections.collection.sync.Collection" , 
                    alpha: float = 0.5,
                    top_k: int = 5
                   ) -> list:
    """
    Performs a hybrid search on a collection and retrieves the top relevant chunks.

    This function executes a hybrid search that combines semantic vector search and traditional 
    keyword-based search on a specified collection to find text chunks most relevant to the 
    input 'query'. The relevance of results is influenced by 'alpha', which balances the weight 
    between vector and keyword matches. It retrieves a limited number of top matching objects, 
    as specified by 'top_k', and returns the 'chunk' property of these objects.

    Args:
    query (str): The search query used to find relevant text chunks.
    collection (weaviate.collections.collection.sync.Collection): The collection in which the hybrid search is performed.
    alpha (float, optional): A weighting factor that balances the contribution of semantic 
    and keyword matches. Defaults to 0.5.
    top_k (int, optional): The number of top relevant objects to retrieve. Defaults to 5.

    Returns:
    List[str]: A list of text chunks that are most relevant to the given query.
    """
    ### START CODE HERE ### 

    # Retrieve using collection.query.hybrid
    response = None

    ### END CODE HERE ###

    response_objects = [x.properties for x in response.objects]

    return response_objects 


# In[ ]:


print_object_properties(hybrid_retrieve('Tell me about the last Taylor Swift show', collection, top_k = 2))


# **Expected Output**
# ```
# article_content: Rapper Killer Mike won three Grammys in the rap category - best rap song, best rap performance and b...(truncated)
# chunk: police brutality and systemic racism. He was a highly visible supporter of Bernie Sanders' two campa...(truncated)
# chunk_index: 4
# description: The 48-year-old was detained on a misdemeanour charge after winning three awards in the rap category.
# link: https://www.bbc.co.uk/news/world-us-canada-68201021?at_medium=RSS&at_campaign=KARANGA
# pubDate: 2024-02-05 23:27:08+00:00
# title: Killer Mike dismisses arrest at Grammys as 'speed bump'
# 
# article_content: Taylor Swift has finished the European leg of her Eras Tour with a record-breaking show at Wembley S...(truncated)
# chunk: size crowd at all". At an earlier show in Liverpool, she had also called the Eras Tour the “most exh...(truncated)
# chunk_index: 10
# description: The star is joined by Florence + The Machine and sings So Long, London at her final UK show.
# link: https://www.bbc.com/news/articles/cr5nr3n6epvo
# pubDate: 2024-08-21 03:02:08+00:00
# title: 'I've never had it this good' - Taylor Swift thanks fans after new Wembley record
# ```

# In[ ]:


unittests.test_hybrid_retrieve(hybrid_retrieve, client)


# ### 5 - Reranking
# 
# <a id='ex05'></a>
# 
# <a id='ex05'></a>
# ### Exercise 5
# 
# In this section, you will create a new version of `semantic_search` that allows reranking of the results. This new function must support using a different query for reranking or reranking based on a specific document property (e.g., reranking using only the title).
# 
# Your task is to add the `rerank` parameter to the `collection.query.near_text` call.
# 
# <details>
# <summary style="color: green;">Hint 1</summary>
# <p>Remember that <code>collection.query.near_text</code> takes a query, a limit (i.e., <code>top_k</code>), and now also requires the <code>rerank</code> parameter.</p>
# </details>
# 
# <details>
# <summary style="color: green;">Hint 2</summary>
# <p>The <code>Rerank</code> object is already loaded into memory. It takes two parameters: the query and the document property to use for ranking—<code>query</code> and <code>prop</code>, respectively.</p>
# </details>
# 
# <details>
# <summary style="color: green;">Hint 3</summary>
# <p>Define the reranker as <code>reranker = Reranker(appropriate_parameters)</code>. Don’t forget: the query for the reranker should be <code>rerank_query</code>!</p>
# </details>

# In[ ]:


# GRADED CELL 

def semantic_search_with_reranking(query: str, 
                                   rerank_property: str,
                                   collection: "weaviate.collections.collection.sync.Collection" , 
                                   rerank_query: str = None,
                                   top_k: int = 5
                                   ) -> list:
    """
    Performs a semantic search and reranks the results based on a specified property.

    Args:
        query (str): The search query to perform the initial search.
        rerank_property (str): The property used for reranking the search results.
        collection (weaviate.collections.collection.sync.Collection): The collection to search within.
        rerank_query (str, optional): The query to use specifically for reranking. If not provided, 
                                      the original query is used for reranking.
        top_k (int, optional): The maximum number of top results to return. Defaults to 5.

    Returns:
        list: A list of properties from the reranked search results, where each item corresponds to 
              an object in the collection.
    """
    ### START CODE HERE ### 

    # Set the rerank_query to be the same as the query if rerank_query is not passed (don't change this line)
    if rerank_query is None: 
        rerank_query = query 

    # Define the reranker with rerank_query and rerank_property
    reranker = None

    # Retrieve using collection.query.near_text with the appropriate parameters (do not forget the rerank!)
    response = None

    ### END CODE HERE ###

    response_objects = [x.properties for x in response.objects]

    return response_objects 


# The reranker model receives a query and a passage (in our case, a chunk of the result) to compute a similarity score.

# In[ ]:


# Set a query
query = 'Tell me about the conflicts in Latin America'
# Get the results from a search (in this case the hybrid search)
results = semantic_search_with_reranking(query, collection = collection, top_k = 2, rerank_property = 'chunk')


# In[ ]:


print_object_properties(results)


# **Expected Results**
# ```
# article_content: A huge diplomatic row has erupted after Spain's transport minister suggested Argentina's president h...(truncated)
# chunk: weeks' to attend the launch of Vox's European election campaign, newspaper El Pais reported. Mr Mile...(truncated)
# chunk_index: 3
# description: A row breaks out after Spain's transport minister suggests Argentina's president has taken drugs.
# link: https://www.bbc.com/news/articles/czd8qzvpl4lo
# pubDate: 2024-05-04 15:56:45+00:00
# title: Spain-Argentina row over drug-use accusation
# 
# article_content: Opposition supporters have gathered across Venezuela to protest against Nicolás Maduro's disputed vi...(truncated)
# chunk: the world, from Australia to Spain and also in the United Kingdom, Canada, Colombia, Mexico and Arge...(truncated)
# chunk_index: 4
# description: Opposition leader María Corina Machado joined thousands of demonstrators in the capital Caracas.
# link: https://www.bbc.com/news/articles/cgedgqqy7x9o
# pubDate: 2024-08-17 23:19:48+00:00
# title: Protests across Venezuela as election dispute goes on
# ```

# In[ ]:


# Test your function!
unittests.test_semantic_search_with_reranking(semantic_search_with_reranking, client)


# <a id='4'></a>
# ## 4 - Incorporating the Weaviate API into our previous schema
# ---
# 
# This section is not graded. Here, you will revisit the functions used throughout the assignments to integrate the Weaviate API into your existing schema. Once integrated, you will be able to run prompts and test your new RAG system!
# 
# <a id='4-1'></a>
# ### 4.1 Generating the final prompt
# 

# In[ ]:


def generate_final_prompt(query: str, 
                          top_k: int, 
                          retrieve_function: callable,
                          rerank_query: str = None, 
                          rerank_property: str = None, 
                          use_rerank: bool = False, 
                          use_rag: bool = True) -> str:
    """
    Generates a final prompt by optionally retrieving and formatting relevant documents using retrieval-augmented generation (RAG).

    Args:
        query (str): The initial query to be used for document retrieval.
        top_k (int): The number of top documents to retrieve and use for generating the prompt.
        retrieve_function (callable): The function used to retrieve documents based on the query.
        rerank_query (str, optional): The query used specifically for reranking documents if reranking is enabled.
        rerank_property (str, optional): The property used for reranking. Required if 'use_rerank' is True.
        use_rerank (bool, optional): Flag to denote whether to use reranking in document retrieval. Defaults to False.
        use_rag (bool, optional): Flag to determine whether to use retrieval-augmented generation. Defaults to True.

    Returns:
        str: A constructed prompt that includes the original query and formatted retrieved documents if 'use_rag' is True.
             Otherwise, it returns the original query.
    """
    # If no rag, return the query
    if not use_rag:
        return query

    if use_rerank:
        if rerank_property is None:
            raise ValueError('rerank_property must be set if use_rerank = True')
        top_k_documents = retrieve_function(query=query, top_k=top_k, collection = collection, rerank_property = rerank_property, rerank_query = rerank_query)
    else:
        top_k_documents = retrieve_function(query=query, top_k=top_k, collection = collection)

    # Initialize an empty string to store the formatted data.
    formatted_data = ""

    # Iterate over each retrieved document.
    for document in top_k_documents:
        # Format each document into a structured string.
        document_layout = (
            f"Title: {document['title']}, Chunk: {document['chunk']}, "
            f"Published at: {document['pubDate']}\nURL: {document['link']}"
        )
        # Append the formatted string to the main data string with a newline for separation.
        formatted_data += document_layout + "\n"

    # If use_rag flag is True, construct the enhanced prompt with the augmented data.
    retrieve_data_formatted = formatted_data  # Store formatted data.
    prompt = (
        f"Answer the user query below. There will be provided additional information for you to compose your answer. "
        f"The relevant information provided is from 2024 and it should be added as your overall knowledge to answer the query, "
        f"you should not rely only on this information to answer the query, but add it to your overall knowledge."
        f"The news data is ordered by relevance."
        f"Query: {query}\n"
        f"2024 News: {retrieve_data_formatted}"
    )

    return prompt


# In[ ]:


prompt = generate_final_prompt("Tell me the economic situation of the US in 2024.", top_k = 5, retrieve_function = semantic_search_retrieve, use_rerank = False, rerank_property = 'title')


# In[ ]:


print(prompt)


# <a id='4-2'></a>
# ### 4.2 LLM call
# 
# Let's revisit the `llm_call` function, now adapted to this assignment.

# In[ ]:


def llm_call(query: str, 
             retrieve_function: callable = None, 
             top_k: int = 5, 
             use_rag: bool = True, 
             use_rerank: bool = False, 
             rerank_property: str = None, 
             rerank_query: str = None) -> str:
    """
    Simulates a call to a language model by generating a prompt and using it to produce a response.

    Args:
        query (str): The initial query for which a response is sought.
        retrieve_function (callable, optional): The function used to retrieve documents related to the query.
        top_k (int, optional): The number of top documents to retrieve and use for generating the prompt. Defaults to 5.
        use_rag (bool, optional): Indicates whether to use retrieval-augmented generation. Defaults to True.
        use_rerank (bool, optional): Indicates whether to apply reranking to the retrieved documents. Defaults to False.
        rerank_property (str, optional): The property to use for reranking. Required if 'use_rerank' is True.
        rerank_query (str, optional): The query used specifically for reranking documents if reranking is enabled.

    Returns:
        str: The generated response content after processing the prompt with a language model.
    """

    # Get the prompt
    PROMPT = generate_final_prompt(query, top_k = top_k, retrieve_function = retrieve_function, use_rag = use_rag, use_rerank = use_rerank, rerank_property = rerank_property, rerank_query = rerank_query)

    generated_response = generate_with_single_input(PROMPT)

    generated_message = generated_response['content']

    return generated_message


# In[ ]:


query = "Tell me about United States and Brazil's relationship over the course of 2024. Provide links for the resources you use in the answer."


# In[ ]:


# Result with reranked results
print(llm_call(query = query, 
               top_k = 5, 
               retrieve_function = hybrid_retrieve, 
               ))


# <a id='5'></a>
# ## 5 - Experimenting with Your RAG System
# 
# Now it is time for you to experiment with the system! Run the next cell to load a widget that will input a query, a rerank property, and output five different LLM responses:
# 
# 1. With semantic search
# 2. With semantic search and reranking
# 3. With BM25 search
# 4. With hybrid search
# 5. Without RAG
# 

# In[ ]:


display_widget(llm_call, semantic_search_retrieve, bm25_retrieve, hybrid_retrieve, semantic_search_with_reranking)


# Congratulations on finishing this assignment!
