def split_string(product_name):
    separators = [',', '/', '\\', '-', ' ']
    # Replace each separator with a space
    for sep in separators:
        product_name = product_name.replace(sep, ' ')
    # Split the modified product_name by space and filter out empty strings
    product_list = list(filter(None, product_name.split(' ')))
    return product_list


# Example usage:
# product_name = "Frequency Converter,VLT FC302,380-500V,IP55,55kW"
# split_result = split_string(product_name)
# print(split_result)
