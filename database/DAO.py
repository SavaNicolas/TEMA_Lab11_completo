from database.DB_connect import DBConnect
from model.arco import Arco
from model.go_products import Go_product


class DAO():
    @staticmethod
    def getAllProducts():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
         FROM go_products g"""
        cursor.execute(query)

        for row in cursor:
            result.append(Go_product(**row))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllColors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct g.Product_color as color
         FROM go_products g"""
        cursor.execute(query)

        for row in cursor:
            result.append(row["color"])
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getProducts_colore(colore):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
             FROM go_products g
             WHERE g.Product_color = %s"""
        cursor.execute(query,(colore,))

        for row in cursor:
            result.append(Go_product(**row))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result

    def addEdges(idMapObjects,colore,anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT s.Product_number as nodo1, s1.Product_number as nodo2,s.`Date`, COUNT(*) as peso
FROM go_products g, go_daily_sales s, go_daily_sales s1
where g.Product_number = s.Product_number and g.Product_color = %s and YEAR(s.`Date`)= %s 
and s.Retailer_code =s1.Retailer_code
and s.`Date` =s1.`Date`
and s.Product_number <> s1.Product_number 
group by s.Product_number, s1.Product_number, s.`Date`"""
        cursor.execute(query,(colore,anno))

        for row in cursor:
            result.append(Arco(idMapObjects[row["nodo1"]],idMapObjects[row["nodo2"]],row["peso"]))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result




