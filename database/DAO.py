from database.DB_connect import DBConnect
from model.DailySale import DailySale
from model.Retailer import Retailer

class DAO():
    def __init__(self):
        pass

    def getAllSales():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from go_daily_sales gds  """

        cursor.execute(query)

        for row in cursor:
            result.append(DailySale(row["Retailer_code"], row["Product_number"], row["Order_method_code"], row["Date"], row["Quantity"], row["Unit_price"], row["Unit_sale_price"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllRetailers():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from go_retailers"""

        cursor.execute(query)

        for row in cursor:
            result.append(Retailer(row["Retailer_code"], row["Retailer_name"], row["Type"], row["Country"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSameProduct(c, a, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = '''SELECT gr1.Retailer_code as Ret1, gr2.Retailer_code as Ret2, COUNT(DISTINCT s1.Product_number) as N
                   FROM go_daily_sales s1, go_daily_sales s2, go_retailers gr1, go_retailers gr2
                   WHERE YEAR(s1.Date) = YEAR(s2.Date)
                   AND YEAR(s1.Date) = %s
                   and gr1.Country = %s
                   and gr2.Country = %s
                   AND gr1.Retailer_code>gr2.Retailer_code
                   AND s1.Product_number = s2.Product_number
                   and s1.Retailer_code = gr1.Retailer_code
                   and s2.Retailer_code = gr2.Retailer_code
                   GROUP BY gr1.Retailer_code, gr2.Retailer_code'''
        cursor.execute(query, (str(a), c, c))

        for row in cursor:
            result.append((idMap[row["Ret1"]], idMap[row["Ret2"]], row["N"]))

        cursor.close()
        conn.close()
        return result


