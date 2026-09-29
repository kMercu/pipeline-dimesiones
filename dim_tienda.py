import sqlite3

def get_connection():
    return sqlite3.connect("data_warehouse.db")

def pipeline_dim_tienda():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = """
            INSERT INTO dim_tienda (tienda_bk, nombre_tienda, ciudad, direccion, fecha_actualizacion)
            SELECT tienda_id, nombre_tienda, ciudad, direccion, DATETIME('now')
            FROM staging_tienda
            WHERE 1=1
            ON CONFLICT(tienda_bk) DO UPDATE SET
                nombre_tienda = excluded.nombre_tienda,
                ciudad = excluded.ciudad,
                direccion = excluded.direccion,
                fecha_actualizacion = DATETIME('now');
        """
        
        cursor.execute(query)
        conn.commit()
        print(f"[dim_tienda] Actualización exitosa. Filas procesadas: {cursor.rowcount}")
        
    except Exception as e:
        conn.rollback()
        print(f"[dim_tienda] Error durante la actualización: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    pipeline_dim_tienda()