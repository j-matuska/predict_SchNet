# -*- coding: utf-8 -*-

# obsolete

def predict(atoms, models, converter):
    
    property_list = []
    # this could be defined in other way. This is very rought; it already in models
    # splits = ["01", "02", "03", "04", "05"]

    
    for at in atoms:
    
        # suradnicove vstupy z xyz #
        inputs = converter(at)
        identifier = str(at.info['name'])
        
        # create dictionary with name and predictions
        line = {}
        
        # add name to dictionary
        line["name"] = identifier
        
        for model in models:
            
            # calculation of prediction
            pred = model.model(inputs)
            predicted_property = pred['DS'].detach().cpu().numpy()[0,0]
            # add prediction to dictionary
            line[model.split] = predicted_property
            
        property_list.append( 
            line 
            )
    
    return property_list