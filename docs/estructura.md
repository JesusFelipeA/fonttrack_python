# Estructura del Proyecto: Tienda Python GUI + MongoDB

## 1. Frontend (Interfaz gráfica con ttkbootstrap)
- `theme_config.py`: Aplica el tema visual global.
- `auth_view.py`: Pantalla única de login y registro.
- `dashboard_view.py`: Redirección según rol del usuario.
- `product_view.py`: Catálogo de productos con botón de compra.
- `cart_view.py`: Visualización del carrito y cálculo total.
- `admin_view.py`: Gestión de usuarios (solo admin).
- `user_view.py`: Perfil del usuario autenticado.
- `main_window.py`: Inicializa la GUI y gestiona navegación.

## 2. Backend (Lógica funcional y conexión a MongoDB)
- `auth_controller.py`: Validación de credenciales y registro.
- `product_controller.py`: Listado, búsqueda y filtrado.
- `cart_controller.py`: Agregado y cálculo del carrito.
- `user_controller.py`: Listado y eliminación de usuarios.
- `db_connection.py`: Conexión centralizada a MongoDB.
- `query_service.py`: Paginación, filtros y búsqueda avanzada.
- `validators.py`: Validación de formularios.
- `formatters.py`: Formato visual de precios, fechas y stock.

## 3. Modelos de datos
- `user_model.py`: Estructura de usuario con rol.
- `product_model.py`: Estructura de producto.
- `order_model.py`: Estructura de orden con items y total.

## 4. Generación de datos simulados
- `generate_products.py`: Crea 500,000 productos con Faker.
- `seed_db.py`: Inserta productos y usuarios con barra de progreso.

## 5. Configuración
- `env.py`: URI de MongoDB y nombres de colección.
- `settings.py`: Tamaño de ventana, tema visual y título.

## 6. Entrada y ejecución
- `main.py`: Punto de entrada del sistema.

## 7. Pruebas unitarias
- `test_auth.py`: Validación de login y registro.
- `test_products.py`: Pruebas de búsqueda y filtros.
- `test_cart.py`: Cálculo de totales y agregados.
- `test_db_connection.py`: Verificación de conexión MongoDB.
