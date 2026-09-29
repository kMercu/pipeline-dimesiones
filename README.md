# Realizado por:
# Naren Santiago Rojas Sánchez
# David Santiago Prieto Beltran

# Pipeline de Actualización de Dimensiones (Esquema Estrella)

Este repositorio contiene los scripts del pipeline de actualización ETL para las tablas maestras de dimensiones de un Data Warehouse.

## Estructura del Proyecto

- `dim_cliente.py`: Pipeline para la dimensión **Cliente** (Estrategia SCD Tipo 1).
- `dim_tienda.py`: Pipeline para la dimensión **Tienda** (Estrategia SCD Tipo 1).
- `dim_producto.py`: Pipeline para la dimensión **Producto** (Estrategia SCD Tipo 2).

## Estrategias Aplicadas

1. **Slowly Changing Dimensions (SCD) Tipo 1:**
   - Aplicado a **Cliente** y **Tienda**.
   - Mantiene la información actualizada directamente mediante sentencias `UPSERT` (`ON CONFLICT DO UPDATE`). Si hay cambios en los atributos del sistema transaccional, se sobrescribe la fila.

2. **Slowly Changing Dimensions (SCD) Tipo 2:**
   - Aplicado a **Producto**.
   - Conserva el historial de cambios de atributos como precios o categorías. Inactiva la versión previa (`es_actual = 0`, `fecha_fin`) e inserta una nueva versión con una nueva *Surrogate Key*.

## Requisitos de Ejecución
- Python 3.x (Utiliza la librería estándar `sqlite3`)