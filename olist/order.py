import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        olist = Olist()
        data = olist.get_data()

        self.orders = data["orders"]
        self.reviews = data["order_reviews"]
        self.order_items = data["order_items"]
        self.order_payments = data["order_payments"]
        self.sellers = data["sellers"]
    def get_wait_time(self, is_delivered=True):
   

    # Orders dataframe'ini kopyala
     orders = self.orders.copy()

    # Sadece delivered siparişler
     if is_delivered:
        orders = orders[orders["order_status"] == "delivered"]

    # Tarih kolonlarını datetime'a çevir
     orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"]
    )
     orders["order_delivered_customer_date"] = pd.to_datetime(
        orders["order_delivered_customer_date"]
    )
     orders["order_estimated_delivery_date"] = pd.to_datetime(
        orders["order_estimated_delivery_date"]
    )

    # Gerçek bekleme süresi (gün, float)
     orders["wait_time"] = (
        orders["order_delivered_customer_date"]
        - orders["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    # Beklenen bekleme süresi (gün, float)
     orders["expected_wait_time"] = (
        orders["order_estimated_delivery_date"]
        - orders["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    # Gecikme: geç geldiyse fark, erken geldiyse 0
     delay = (
        orders["order_delivered_customer_date"]
        - orders["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

     orders["delay_vs_expected"] = np.where(delay > 0, delay, 0)

    # İstenen kolonları döndür
     return orders[
        [
            "order_id",
            "wait_time",
            "expected_wait_time",
            "delay_vs_expected",
            "order_status",
        ]
    ]

    
    

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        

        reviews = self.reviews.copy()

    # review_score NaN olmasın
        reviews = reviews.dropna(subset=["review_score"])

    # int'e çevir
        reviews["review_score"] = reviews["review_score"].astype(int)

    # Dummy kolonlar
        reviews["dim_is_five_star"] = (reviews["review_score"] == 5).astype(int)
        reviews["dim_is_one_star"] = (reviews["review_score"] == 1).astype(int)

        return reviews[
        [
            "order_id",
            "review_score",
            "dim_is_five_star",
            "dim_is_one_star",
        ]
    ]

        

    def get_number_items(self):
        """
        Returns a DataFrame with:
        order_id, number_of_items
        """
        order_items = self.order_items.copy()

        number_of_items = (
              order_items
       .groupby("order_id")
        .size()
        .reset_index(name="number_of_items")
    )

        return number_of_items
        
        

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_isd, number_of_sellers
        """
        order_items = self.order_items.copy()

        number_of_sellers = (
        order_items
        .groupby("order_id")["seller_id"]
        .nunique()
        .reset_index(name="number_of_sellers")
    )

        return number_of_sellers
        

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        
        order_items = self.order_items.copy()

        price_freight = (
        order_items
        .groupby("order_id")[["price", "freight_value"]]
        .sum()
        .reset_index()
    )

        return price_freight
        
        
        
        

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        pass  # YOUR CODE HERE

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_items', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        df = self.get_wait_time()

    # 2) Review score
        reviews = self.get_review_score()
        df = df.merge(reviews, on="order_id", how="left")

    # 3) Number of items
        items = self.get_number_items()
        df = df.merge(items, on="order_id", how="left")

    # 4) Number of sellers
        sellers = self.get_number_sellers()
        df = df.merge(sellers, on="order_id", how="left")

    # 5) Price & freight
        price_freight = self.get_price_and_freight()
        df = df.merge(price_freight, on="order_id", how="left")

    # 6) NaN temizliği
        df = df.dropna()

        return df
      
