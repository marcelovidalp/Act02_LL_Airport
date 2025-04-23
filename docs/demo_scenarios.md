# Escenarios de Demostración - Sistema de Gestión de Aeropuerto

Este documento presenta escenarios prácticos para demostrar las funcionalidades del Sistema de Gestión de Aeropuerto. Son ideales para mostrar en un video o presentación.

## Escenario 1: Gestión Básica de Vuelos

### Paso 1: Crear y Listar Vuelos
1. Crear un nuevo vuelo:
   ```http
   POST /api/vuelos/
   Content-Type: application/json
   
   {
     "codigo": "BA2490",
     "origen": "Londres",
     "destino": "Madrid",
     "aerolinea": "British Airways",
     "estado": "programado"
   }
   ```

2. Listar todos los vuelos:
   ```http
   GET /api/vuelos/
   ```

### Paso 2: Añadir Vuelos a una Lista
1. Añadir el vuelo al final de la lista:
   ```http
   POST /api/vuelos
   Content-Type: application/json
   
   {
     "codigo": "IB3512",
     "origen": "Madrid",
     "destino": "Barcelona",
     "aerolinea": "Iberia",
     "estado": "programado"
   }
   ```

2. Añadir vuelo prioritario al inicio de la lista:
   ```http
   POST /api/vuelos?position=first
   Content-Type: application/json
   
   {
     "codigo": "AF2382",
     "origen": "París",
     "destino": "Madrid",
     "aerolinea": "Air France",
     "estado": "emergencia"
   }
   ```

3. Ver la lista completa de vuelos:
   ```http
   GET /api/vuelos/lista
   ```

### Paso 3: Consultar Posiciones Específicas
1. Ver el primer vuelo (próximo):
   ```http
   GET /api/vuelos/proximo
   ```

2. Ver el último vuelo:
   ```http
   GET /api/vuelos/ultimo
   ```

3. Contar el total de vuelos:
   ```http
   GET /api/vuelos/total
   ```

## Escenario 2: Manipulación de la Lista

### Paso 1: Insertar en Posición Específica
1. Insertar un vuelo en la posición 1:
   ```http
   POST /api/vuelos/insertar?position=1
   Content-Type: application/json
   
   {
     "codigo": "LH1826",
     "origen": "Frankfurt",
     "destino": "Madrid",
     "aerolinea": "Lufthansa",
     "estado": "programado"
   }
   ```

2. Ver la lista actualizada:
   ```http
   GET /api/vuelos/lista
   ```

### Paso 2: Extraer de Posición Específica
1. Extraer el vuelo en posición 1:
   ```http
   DELETE /api/vuelos/extraer?position=1
   ```

2. Ver la lista actualizada:
   ```http
   GET /api/vuelos/lista
   ```

### Paso 3: Reordenar Vuelos
1. Mover el vuelo de la posición 0 a la posición 2:
   ```http
   PATCH /api/vuelos/reordenar?from_pos=0&to_pos=2
   ```

2. Ver la lista reordenada:
   ```http
   GET /api/vuelos/lista
   ```

## Escenario 3: Priorización y Estados de Vuelos

### Paso 1: Crear Vuelos con Diferentes Estados
1. Crear vuelos con varios estados:
   ```http
   POST /api/vuelos/
   Content-Type: application/json
   
   {
     "codigo": "VY1234",
     "origen": "Barcelona",
     "destino": "Sevilla",
     "aerolinea": "Vueling",
     "estado": "embarque"
   }
   ```

   ```http
   POST /api/vuelos/
   Content-Type: application/json
   
   {
     "codigo": "IB5678",
     "origen": "Madrid",
     "destino": "Valencia",
     "aerolinea": "Iberia",
     "estado": "retrasado"
   }
   ```

   ```http
   POST /api/vuelos/
   Content-Type: application/json
   
   {
     "codigo": "FR9012",
     "origen": "Dublín",
     "destino": "Madrid",
     "aerolinea": "Ryanair",
     "estado": "emergencia"
   }
   ```

2. Añadir todos a la lista:
   ```http
   POST /api/vuelos?position=last&lista_id=1
   Content-Type: application/json
   
   // Repetir para cada vuelo creado anteriormente
   ```

### Paso 2: Priorizar Vuelos
1. Ejecutar la priorización:
   ```http
   POST /api/listas/1/priorizar
   ```

2. Ver la lista priorizada:
   ```http
   GET /api/vuelos/lista
   ```
   
   Ahora los vuelos deberían aparecer en este orden:
   1. Vuelos en estado EMERGENCIA
   2. Vuelos en estado EMBARQUE
   3. Vuelos en estado PROGRAMADO
   4. Vuelos en otros estados

### Paso 3: Cambiar Estado de un Vuelo
1. Cambiar el estado de un vuelo:
   ```http
   PATCH /api/vuelos/1/estado
   Content-Type: application/json
   
   {
     "estado": "despegado"
   }
   ```

2. Priorizar de nuevo:
   ```http
   POST /api/listas/1/priorizar
   ```

3. Ver la lista actualizada:
   ```http
   GET /api/vuelos/lista
   ```

## Escenario 4: Caso de Uso Completo - Gestión de Crisis

Este escenario simula la gestión de una crisis aeroportuaria con múltiples cambios de estado y priorizaciones.

### Paso 1: Configuración Inicial
1. Crear y añadir varios vuelos con diferentes estados

### Paso 2: Simulación de Emergencia
1. Cambiar el estado de un vuelo a emergencia
2. Priorizar la lista
3. Verificar que el vuelo en emergencia esté al inicio

### Paso 3: Resolución de la Emergencia
1. Cambiar el estado del vuelo de emergencia a aterrizado
2. Priorizar la lista
3. Verificar que el vuelo ya no está en la posición prioritaria

### Paso 4: Nuevos Embarques
1. Cambiar estados de algunos vuelos a embarque
2. Priorizar la lista
3. Verificar el nuevo orden según las prioridades

Este escenario demuestra cómo el sistema puede adaptarse dinámicamente a situaciones cambiantes en el aeropuerto, asegurando que los vuelos más críticos siempre reciban atención prioritaria.

## Consejos para la Demostración en Video

1. **Narración Clara**: Explica cada paso mientras lo ejecutas
2. **Visualización**: Muestra tanto las peticiones HTTP como las respuestas
3. **Comparación**: Haz capturas de la lista antes y después de cada operación
4. **Explicación Conceptual**: Relaciona cada operación con el concepto de lista enlazada
5. **Casos de Uso Reales**: Explica cómo cada función se aplicaría en un aeropuerto real
