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
    
    @staticmethod
    def addEdges(idU,idV,idMapObjects,anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT s.Product_number as nodo1, s1.Product_number as nodo2, s.`Date`
FROM go_daily_sales s, go_daily_sales s1
WHERE YEAR(s.`Date`)= %s and s.`Date` = s1.`Date` and s.Retailer_code = s1.Retailer_code
and s.Product_number=%s and s1.Product_number=%s
group by s.Product_number, s1.Product_number,s.`Date`"""
        cursor.execute(query,(anno,idU,idV))
        #devo fare la group by anche sul rivenditore per evitare che ci siano doppioni di p1,p2,rivenditore1

        for row in cursor:
            result.append(Arco(idMapObjects[row["nodo1"]],idMapObjects[row["nodo2"]]))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result




