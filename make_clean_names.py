import pandas as pd
import re
import unicodedata

def clean_column_names(df, case="snake", replace={"'": "", '"': "", "%": "_percent_", "#": "_number_"}, ascii=True, allow_dupes=False):
    def clean_name(name):
        # Replace specified characters
        for key, value in replace.items():
            name = name.replace(key, value)
        
        # Transliterate to ASCII if needed
        if ascii:
            name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
        
        # Remove leading and trailing whitespace and special characters
        name = re.sub(r'^[\s\W_]+|[\s\W_]+$', '', name)
        
        # Replace spaces and special characters with underscores
        name = re.sub(r'[\s\W_]+', '_', name)
        
        # Convert to specified case
        if case == "snake":
            name = name.lower()
        elif case == "camel":
            name = ''.join(word.capitalize() if i != 0 else word for i, word in enumerate(name.split('_')))
        elif case == "kebab":
            name = name.lower().replace('_', '-')
        
        return name
    
    # Clean column names
    cleaned_names = [clean_name(col) for col in df.columns]
    
    # Handle duplicate names
    if not allow_dupes:
        seen = {}
        for i, name in enumerate(cleaned_names):
            if name in seen:
                seen[name] += 1
                cleaned_names[i] = f"{name}_{seen[name]}"
            else:
                seen[name] = 0
    
    df.columns = cleaned_names
    return df
