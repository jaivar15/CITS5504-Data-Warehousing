def rename_binary_attributes(data, attribute):
    for index in attribute:  
        data[attribute] = data[attribute].replace(['Yes', 'YES', 'has','Has','yes'],'yes')
        data[attribute] = data[attribute].replace(['NO', 'not', 'Not','No','no'],'no')
    return data
mobile_data = rename_binary_attributes(mobile_data, ['blue','dual_sim','three_g','wifi'])