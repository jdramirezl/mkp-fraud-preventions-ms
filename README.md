# Fraud Prevention Microservice

Un microservicio robusto desarrollado en TypeScript para la detección y prevención de fraudes en transacciones digitales.

## 📋 Características

- **Evaluación de riesgo en tiempo real** - Análisis automático de transacciones para determinar niveles de riesgo
- **Seguimiento de usuarios y dispositivos** - Monitoreo de patrones de comportamiento sospechosos
- **API RESTful completa** - Endpoints para todas las operaciones CRUD
- **Bloqueo de transacciones** - Capacidad para bloquear transacciones sospechosas con registro de motivos
- **Persistencia en MySQL** - Almacenamiento seguro y eficiente de los datos
- **Containerizado con Docker** - Facilidad de despliegue en cualquier entorno

## 🚀 Instalación

### Prerrequisitos

- Node.js (v18 o superior)
- npm o yarn
- Docker y Docker Compose (opcional, para entorno containerizado)

### Configuración Local

1. **Clonar el repositorio**

```bash
git clone <url-del-repositorio>
cd fraud-preventions-ms
```

2. **Instalar dependencias**

```bash
npm install
```

3. **Configurar variables de entorno**

Crea un archivo `.env` en la raíz del proyecto basándote en el ejemplo:

```
# Database configuration
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=root
DB_PASSWORD=password
DB_DATABASE=fraud_prevention

# Server configuration
PORT=3000
NODE_ENV=development
```

4. **Iniciar el servidor en modo desarrollo**

```bash
npm run dev
```

### Usando Docker

1. **Construir y levantar los contenedores**

```bash
docker-compose up -d
```

Este comando iniciará tanto el microservicio como la base de datos MySQL.

## 🛠️ Arquitectura

El microservicio sigue una arquitectura en capas:

```
fraud-preventions-ms/
├── src/
│   ├── controllers/     # Manejo de peticiones HTTP
│   ├── datasource/      # Configuración de conexión a base de datos
│   ├── entity/          # Definición de entidades y modelos
│   ├── routes/          # Definición de rutas de la API
│   ├── services/        # Lógica de negocio
│   └── index.ts         # Punto de entrada de la aplicación
```

## 📡 API Endpoints

### Prevención de Fraude

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/fraud-preventions` | Obtener todas las prevenciones de fraude (paginado) |
| GET | `/api/fraud-preventions/:id` | Obtener una prevención de fraude por ID |
| GET | `/api/fraud-preventions/transaction/:transactionId` | Obtener prevención por ID de transacción |
| GET | `/api/fraud-preventions/user/:userId` | Obtener todas las prevenciones de un usuario |
| POST | `/api/fraud-preventions` | Crear nuevo registro de prevención de fraude |
| PUT | `/api/fraud-preventions/:id` | Actualizar un registro existente |
| DELETE | `/api/fraud-preventions/:id` | Eliminar un registro |
| POST | `/api/fraud-preventions/:id/block` | Bloquear una transacción con razón específica |

### Salud del Servicio

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Verificar el estado del servicio |

## 📥 Ejemplos de Uso

### Crear una nueva verificación de fraude

```bash
curl -X POST http://localhost:3000/api/fraud-preventions \
  -H "Content-Type: application/json" \
  -d '{
    "transactionId": "tx-123456789",
    "userIp": "192.168.1.1",
    "deviceId": "device-xyz-123",
    "userId": "user-abc-456",
    "additionalData": {
      "amount": 1000,
      "currency": "USD",
      "paymentMethod": "credit_card"
    }
  }'
```

### Bloquear una transacción sospechosa

```bash
curl -X POST http://localhost:3000/api/fraud-preventions/uuid-del-registro/block \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Múltiples intentos fallidos desde diferentes ubicaciones"
  }'
```

## 📊 Modelo de Datos

La entidad principal `FraudPrevention` contiene:

- `id`: Identificador único (UUID)
- `transactionId`: ID de la transacción relacionada
- `userIp`: Dirección IP del usuario
- `deviceId`: Identificador del dispositivo usado
- `userId`: Identificador del usuario
- `riskLevel`: Nivel de riesgo (LOW, MEDIUM, HIGH, CRITICAL)
- `additionalData`: Datos adicionales de la transacción (JSON)
- `isBlocked`: Indicador si la transacción está bloqueada
- `blockReason`: Razón del bloqueo
- `attemptCount`: Contador de intentos
- `createdAt`: Fecha de creación
- `updatedAt`: Fecha de actualización

## 🧪 Tests

Para ejecutar las pruebas:

```bash
npm run test
```

## 🔄 Ciclo de Desarrollo

1. **Compilar TypeScript**

```bash
npm run build
```

2. **Lint del código**

```bash
npm run lint
```

3. **Ejecutar servidor compilado**

```bash
npm start
```

## 🚢 Despliegue

### En Producción

1. Configurar variables de entorno para producción
2. Construir la imagen Docker:

```bash
docker build -t fraud-preventions-ms:latest .
```

3. Ejecutar con la configuración adecuada:

```bash
docker run -p 3000:3000 --env-file .env.production fraud-preventions-ms:latest
```

## 📚 Documentación Adicional

Para una documentación interactiva de la API, considera implementar Swagger:

```bash
# TODO: Agregar instrucciones para configurar Swagger
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit de tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo [LICENCIA] - ver el archivo LICENSE.md para más detalles.

## 📞 Contacto

[Nombre del equipo/desarrollador] - [email]

---

Desarrollado con ❤️ por [Tu nombre/equipo]
