**Nombre del documento**

`3-CasosUsoUML-BotAsistenciaInternaTelegram.md`

---

**Contenido requerido**

1. Encabezado

   ```
   # Modelo de Casos de Uso – Bot de Asistencia Interna vía Telegram
   Versión: 1.0  
   Fecha: AAAA-MM-DD
   ```

2. Propósito
   Describir gráficamente y en texto los casos de uso que cubre el sistema, delimitando actores y flujos.

3. Diagrama general de casos de uso

   ```mermaid
   %% UML Use Case Diagram
   left to right direction
   actor Operario
   actor Supervisor
   actor ResponsableCalidad
   rectangle SistemaBot {
       (CU1 Consultar stock) as CU1
       (CU2 Consultar procedimiento ISO) as CU2
       (CU3 Generar respuesta con Gemini) as CU3
       (CU4 Registrar interacción) as CU4
       (CU5 Sincronizar stock) as CU5
       (CU6 Importar documentos ISO) as CU6
   }
   Operario -- CU1
   Operario -- CU2
   Supervisor -- CU1
   ResponsableCalidad -- CU2
   CU3 <-- CU1
   CU3 <-- CU2
   CU4 <-- CU1
   CU4 <-- CU2
   CU5 ..> CU1 : incluye
   CU6 ..> CU2 : incluye
   ```

4. Tabla de actores

   | Actor              | Descripción                                  | Tipo       |
   | ------------------ | -------------------------------------------- | ---------- |
   | Operario           | Usuario que consulta stocks y procedimientos | Primario   |
   | Supervisor         | Usuario que verifica stock y reportes        | Primario   |
   | ResponsableCalidad | Usuario que consulta ISO 9001                | Primario   |
   | SistemaBot         | Aplicación Django que procesa peticiones     | Sistema    |
   | API Telegram       | Servicio externo que entrega webhooks        | Secundario |
   | Google Sheets API  | Fuente de datos de stock                     | Secundario |
   | Google Drive API   | Fuente de documentos ISO                     | Secundario |
   | Gemini API         | Generador de respuestas contextuales         | Secundario |

5. Descripción textual de casos de uso

| CU  | Nombre                       | Actor primario     | Objetivo                              | Precondiciones                   | Flujo principal                                                                                                                                                                           | Postcondición                                     |
| --- | ---------------------------- | ------------------ | ------------------------------------- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| CU1 | Consultar stock              | Operario           | Obtener cantidad disponible de un SKU | Bot registrado como webhook      | 1. Operario envía mensaje con SKU<br>2. Bot consulta MySQL (tabla `product_stock`)<br>3. Bot genera prompt con stock y pregunta<br>4. Bot invoca CU3<br>5. Bot envía respuesta a Operario | Mensaje de stock enviado y CU4 registrado         |
| CU2 | Consultar procedimiento ISO  | ResponsableCalidad | Recuperar texto de procedimiento      | Documento ISO cargado en base    | 1. Usuario envía palabra clave<br>2. Bot busca coincidencia LIKE en `iso_documents`<br>3. Bot agrega extracto al prompt<br>4. Invoca CU3<br>5. Envía respuesta                            | Mensaje con extracto ISO enviado y CU4 registrado |
| CU3 | Generar respuesta con Gemini | SistemaBot         | Construir texto de respuesta          | Clave API válidas                | 1. Bot envía prompt a Gemini<br>2. Recibe texto<br>3. Devuelve a CU1/CU2                                                                                                                  | Texto disponible para envío                       |
| CU4 | Registrar interacción        | SistemaBot         | Guardar trazabilidad                  | Base `telegram_update` operativa | 1. Registrar mensaje y respuesta con timestamp                                                                                                                                            | Registro persistente                              |
| CU5 | Sincronizar stock            | SistemaBot         | Actualizar tabla `product_stock`      | Acceso a Google Sheets           | 1. Script lee hoja<br>2. Actualiza MySQL                                                                                                                                                  | Datos actualizados                                |
| CU6 | Importar documentos ISO      | SistemaBot         | Cargar Markdown ISO                   | Archivos disponibles             | 1. Script lee archivos<br>2. Actualiza `iso_documents`                                                                                                                                    | Documentos actualizados                           |

6. Reglas de negocio asociadas

   * RB-01: Un SKU debe existir en `product_stock` para responder CU1.
   * RB-02: Documentos ISO se identifican de forma única por título.

7. Requisitos de trazabilidad
   Tabla que relacione cada CU con los requisitos funcionales del SRS.

8. Versionado
   Historial de cambios con fecha, autor y descripción.
