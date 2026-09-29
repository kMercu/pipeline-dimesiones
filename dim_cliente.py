import sqlite3

def get_connection():
    return sqlite3.connect("data_warehouse.db")

def pipeline_dim_cliente():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = """
            INSERT INTO dim_cliente (cliente_bk, nombre, email, telefono, fecha_actualizacion)
            SELECT cliente_id, nombre, email, telefono, DATETIME('now')
            FROM staging_cliente
            WHERE 1=1
            ON CONFLICT(cliente_bk) DO UPDATE SET
                nombre = excluded.nombre,
                email = excluded.email,
                telefono = excluded.telefono,
                fecha_actualizacion = DATETIME('now');
        """
        
        cursor.execute(query)
        conn.commit()
        print(f"[dim_cliente] Actualización exitosa. Filas procesadas: {cursor.rowcount}")
        
    except Exception as e:
        conn.rollback()
        print(f"[dim_cliente] Error durante la actualización: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    pipeline_dim_cliente()