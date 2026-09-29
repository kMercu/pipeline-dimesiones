import sqlite3

def get_connection():
    return sqlite3.connect("data_warehouse.db")

def pipeline_dim_producto():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query_inactivar = """
            UPDATE dim_producto
            SET fecha_fin = DATE('now', '-1 day'),
                es_actual = 0
            WHERE es_actual = 1
              AND producto_bk IN (
                  SELECT stg.producto_id
                  FROM staging_producto stg
                  JOIN dim_producto dim ON stg.producto_id = dim.producto_bk AND dim.es_actual = 1
                  WHERE dim.categoria != stg.categoria OR dim.precio_base != stg.precio_base
              );
        """
        cursor.execute(query_inactivar)
        
        query_insertar = """
            INSERT INTO dim_producto (producto_bk, nombre_producto, categoria, precio_base, fecha_inicio, fecha_fin, es_actual)
            SELECT 
                stg.producto_id,
                stg.nombre_producto,
                stg.categoria,
                stg.precio_base,
                DATE('now'),
                NULL,
                1
            FROM staging_producto stg
            LEFT JOIN dim_producto dim 
                   ON stg.producto_id = dim.producto_bk AND dim.es_actual = 1
            WHERE dim.producto_key IS NULL 
               OR dim.categoria != stg.categoria 
               OR dim.precio_base != stg.precio_base;
        """
        cursor.execute(query_insertar)
        
        conn.commit()
        print("[dim_producto] Actualización SCD Tipo 2 completada con éxito.")
        
    except Exception as e:
        conn.rollback()
        print(f"[dim_producto] Error durante la actualización: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    pipeline_dim_producto()