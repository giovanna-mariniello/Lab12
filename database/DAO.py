from database.DB_connect import DBConnect
from model.Retailer import Retailer


class DAO():
    @staticmethod
    def get_all_nazioni():

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = []

        query = """ SELECT DISTINCT Country
                    FROM go_retailers"""

        cursor.execute(query)
        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_all_anni():

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = []

        query = """ select distinct YEAR(gds.Date) as Year
                    from go_daily_sales gds """

        cursor.execute(query)
        for row in cursor:
            result.append(row["Year"])

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_retailers_nazione(nazione):

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = []

        query = """ select gr.*
                    from go_retailers gr 
                    where gr.Country = %s """

        cursor.execute(query, (nazione,))
        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_archi(nazione, anno, idMap_retailers):

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = []

        query = """  select gds1.Retailer_code as r1, gds2.Retailer_code as r2 ,COUNT(DISTINCT(gds2.Product_number)) as N
                    from go_daily_sales gds1 , go_retailers gr1, go_daily_sales gds2, go_retailers gr2
                    where gds1.Product_number = gds2.Product_number 
                    and gds1.Retailer_code = gr1.Retailer_code
                    and gds2.Retailer_code = gr2.Retailer_code 
                    and YEAR(gds1.`Date`) = YEAR(gds2.`Date`)
                    and year(gds2.`Date`) = %s
                    and gr1.Country = gr2.Country 
                    and gr1.Country = %s 
                    and gds1.Retailer_code < gds2.Retailer_code 
                    group by gds1.Retailer_code, gds2.Retailer_code """

        cursor.execute(query, (anno, nazione, ))
        for row in cursor:
            ret1 = idMap_retailers[row["r1"]]
            ret2 = idMap_retailers[row["r2"]]
            peso = row["N"]

            result.append((ret1, ret2, peso))

        cursor.close()
        cnx.close()
        return result



