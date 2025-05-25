**Nombre del documento**

`2-ContextoStakeholders-BotAsistenciaInternaTelegram.md`

---

**Contenido indicado**

1. **Propósito del documento**
   Breve párrafo que establezca la finalidad: mostrar en alto nivel las interacciones externas del sistema y detallar actores involucrados.

2. **Diagrama de contexto**

   * Representación en notación C4 nivel 1 o diagrama de flujo simple.
   * Elementos obligatorios:

     * Usuario Telegram
     * Servidor Django (Bot)
     * ngrok (túnel HTTPS)
     * Telegram Bot API
     * Google Sheets API
     * Google Drive API
     * Gemini API
     * MySQL
   * Flechas etiquetadas con tipo de mensaje (HTTP POST, REST GET, SQL, etc.).

   ```mermaid
   graph TD
       UT[Usuario Telegram]
       UT -- Mensaje --> TB[Telegram Bot API]
       TB -- Webhook JSON --> NG[ngrok túnel]
       NG -- HTTP --> DJ[Django Bot]
       DJ -- SQL --> DB[MySQL]
       DJ -- REST --> GS[Google Sheets API]
       DJ -- REST --> GD[Google Drive API]
       DJ -- REST --> GM[Gemini API]
   ```

3. **Descripción de stakeholders**

| Actor / Rol                 | Tipo (Interno/Externo) | Interés principal                 | Expectativa clave                          |
| --------------------------- | ---------------------- | --------------------------------- | ------------------------------------------ |
| Operario                    | Interno                | Consultar stock y procedimientos  | Respuesta rápida y precisa                 |
| Supervisor de Producción    | Interno                | Verificar datos de stock          | Disponibilidad y fiabilidad                |
| Responsable de Calidad      | Interno                | Acceder a procedimientos ISO 9001 | Actualización constante de documentos      |
| Equipo de TI                | Interno                | Implementar y mantener el sistema | Código mantenible, logs de auditoría       |
| Usuario Telegram (genérico) | Externo                | Enviar/recibir mensajes           | Funcionamiento continuo del bot            |
| Google Cloud APIs           | Externo                | Proveer datos y procesamiento     | Autenticación válida, límites respetados   |
| Telegram Bot API            | Externo                | Entregar actualizaciones webhooks | URL HTTPS alcanzable                       |
| Gemini API                  | Externo                | Generar respuestas mediante LLM   | Cumplimiento de cuota y latencia aceptable |

4. **Relaciones y flujos de información**
   Texto técnico que explique por qué cada actor se comunica con el sistema, qué datos intercambia y con qué frecuencia.

5. **Suposiciones**

   * Conectividad a Internet estable para acceder a Google y Telegram.
   * ngrok operativo durante la sesión.
   * Autorizaciones API configuradas.

6. **Dependencias identificadas**

   * Token de bot válido.
   * Credenciales de servicio Google.
   * Clave API Gemini.

7. **Referencias cruzadas**
   Enlaces al SRS (`1-SRS-BotAsistenciaInternaTelegram.d`) y a la Visión y Alcance (`0-VisionAlcance-BotAsistenciaInternaTelegram.d`).
