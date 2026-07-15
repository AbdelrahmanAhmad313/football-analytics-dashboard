from analytics.analytics import METRIC_REGISTRY



def interpretCorrelation(corr,metric1,metric2):
    # very strong 1-0.75 - Strong 0.75 -0.5- weak 0.5-0.25 - very weak 0.25-0.01
    # positive (+)- negative(-)
    # no relation 0.0
    label1=METRIC_REGISTRY[metric1]["label"]
    label2=METRIC_REGISTRY[metric2]["label"]

    insight=""
    comment=f"Teams with higher {label1} tend to have "
    if (abs(corr)<0.1):
        insight="No Relation"
        comment = f"No meaningful relationship was found between {label1} and {label2}."
            
        return insight,comment
    
    if(abs(corr)>=0.75):
        insight+="Very Strong "
        comment+="very strong "
    elif(abs(corr)>=0.5):
        insight+="Strong "
        comment+="strong "
    elif(abs(corr)>=0.25):
        insight+="Weak "
        comment+="weak "
    else:
        insight+="Very Weak "
        comment+="very weak "
    
    if (corr>0):
        insight+="Positive "
        comment+="positive "
    else:
        insight+="Negative "
        comment+="negative "
        
    insight+="Correlation "
    comment+=f"realtionship with {label2}"
    
    return insight, comment


