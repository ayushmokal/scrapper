import pandas as pd
from datetime import datetime

def save_to_csv(doctors, zip_code):
    """Save doctor information to a CSV file."""
    if not doctors:
        return None
        
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"doctors_{zip_code}_{date_str}.csv"
    
    df = pd.DataFrame(doctors)
    df.to_csv(filename, index=False)
    
    return filename