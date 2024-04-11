from func_string import split_string
from func_db import get_database_config, get_data_from_db_by_sqlString


def calculate_similarity(text, products):
    # Split the input text into a list of strings
    input_strings = split_string(text)
    
    # Initialize a list to store similarity scores for each product
    similarity_scores = []
    
    # Iterate over each product from the database
    for product in products:
        # Extract ITEM_ID and ITEM_NAME from the product
        item_id = product[0]
        item_name = product[1]

        # Split the product name into individual words
        product_words = split_string(item_name)  

        # Initialize a variable to store the total similarity score for this product
        total_similarity = 0
        
        # Iterate over each string in the input text
        for string in input_strings:
            # Check if the string exists in the current product
            if string in product_words:
                # If a match is found, increment the total similarity score
                total_similarity += 1 / len(input_strings)
        
        # Convert the total similarity score to percentage
        similarity_percent = total_similarity * 100
        
        # Append the total similarity score for this product to the list
        similarity_scores.append([item_id, item_name, similarity_percent])
    
    return similarity_scores

# Example usage:
config_filename = 'config.json'
config = get_database_config(config_filename)
sqlString = "select top 100 ITEM_ID, ITEM_NAME from usv_Ax_InventTable"
products = get_data_from_db_by_sqlString(config, sqlString)

text = "Name Plate"
similarity_scores = calculate_similarity(text, products)
print("Similarity Scores:", similarity_scores)
