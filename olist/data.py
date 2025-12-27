from pathlib import Path
import pandas as pd


class Olist:
    """
    The Olist class provides methods to interact with Olist's e-commerce data.

    Methods:
        get_data():
            Loads and returns a dictionary where keys are dataset names (e.g., 'sellers', 'orders')
            and values are pandas DataFrames loaded from corresponding CSV files.

        ping():
            Prints "pong" to confirm the method is callable.
    """
    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrames loaded from csv files
        """
        
        csv_path = Path.home() / ".workintech/olist/data/csv"
        csv_files = list(csv_path.iterdir())

        data = {}
        for file in csv_files:
         table_name = ( file.name.replace("olist_", "").replace("_dataset.csv", "").replace(".csv", "")
         )
         data[table_name] = pd.read_csv(file)

        return data
        
        
        #pass 

    def ping(self):
        """
        Prints 'pong' to confirm the method is callable.
    
        """
        print("pong")