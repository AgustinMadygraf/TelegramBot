**Nombre del documento**

`5-DER-DDL-BotAsistenciaInternaTelegram.d`

---

## Contenido recomendado

| Sección                            | Descripción técnica                                                                                                                  |   |    |   |                                   |   |                                                      |   |                            |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | - | -- | - | --------------------------------- | - | ---------------------------------------------------- | - | -------------------------- |
| 1  Propósito                       | Definir el modelo relacional (DER) y suministrar los scripts DDL para crear la base de datos MySQL 8.2 del bot.                      |   |    |   |                                   |   |                                                      |   |                            |
| 2  Diagrama Entidad-Relación       | ER a nivel lógico con cardinalidades 1\:N. Puede emplearse notación Mermaid:<br><br>\`\`\`mermaid<br>erDiagram<br>    PRODUCT\_STOCK |   | .. |   | SKU : tiene<br>    ISO\_DOCUMENTS |   | --o{ KEYWORD : contiene<br>    TELEGRAM\_UPDATE }o-- |   | CHAT : pertenece<br>\`\`\` |
| 3  Descripción de entidades        | Tabla por entidad con campos, tipo, PK, NN, default, descripción funcional.                                                          |   |    |   |                                   |   |                                                      |   |                            |
| 4  DDL completo                    | Scripts `CREATE DATABASE`, `CREATE TABLE`, índices, claves foráneas, collation `utf8mb4_unicode_ci`.                                 |   |    |   |                                   |   |                                                      |   |                            |
| 5  Índices adicionales             | Índices compuestos para búsqueda por `sku`, `keyword`, `chat_id`.                                                                    |   |    |   |                                   |   |                                                      |   |                            |
| 6  Procedimientos de carga inicial | Ejemplo de `INSERT` para datos de referencia (SKU de prueba).                                                                        |   |    |   |                                   |   |                                                      |   |                            |
| 7  Políticas de integridad         | Restricciones de clave externa, reglas de cascada o `ON DELETE RESTRICT`.                                                            |   |    |   |                                   |   |                                                      |   |                            |
| 8  Historial de versiones          | Fecha, número de versión, descripción de cambio.                                                                                     |   |    |   |                                   |   |                                                      |   |                            |

### Ejemplo de DDL resumido

```sql
-- 1. Base
CREATE DATABASE bot_db 
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;
USE bot_db;

-- 2. producto_stock
CREATE TABLE product_stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(64) NOT NULL,
    description VARCHAR(255),
    quantity INT NOT NULL DEFAULT 0,
    updated_at DATETIME NOT NULL,
    UNIQUE KEY uq_sku (sku)
) ENGINE=InnoDB;

-- 3. iso_documents
CREATE TABLE iso_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    body LONGTEXT NOT NULL,
    updated_at DATETIME NOT NULL,
    FULLTEXT KEY ft_body (body)
) ENGINE=InnoDB 
  ROW_FORMAT=DYNAMIC;

-- 4. telegram_update
CREATE TABLE telegram_update (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    user_message TEXT NOT NULL,
    bot_answer TEXT,
    ts DATETIME NOT NULL,
    INDEX idx_chat_ts (chat_id, ts)
) ENGINE=InnoDB;

-- 5. keywords (opcional, mejora búsqueda ISO)
CREATE TABLE keyword (
    id INT AUTO_INCREMENT PRIMARY KEY,
    iso_doc_id INT NOT NULL,
    word VARCHAR(64) NOT NULL,
    FOREIGN KEY (iso_doc_id) REFERENCES iso_documents(id) 
        ON DELETE CASCADE,
    INDEX idx_word (word)
) ENGINE=InnoDB;
```

> **Nota:** el índice FULLTEXT sobre `body` permite búsquedas rápidas de términos en textos ISO. El índice compuesto `idx_chat_ts` acelera consultas por chat y fecha.

### Derivación a partir del esquema

* **product\_stock** almacena inventario; clave única `sku`.
* **iso\_documents** reúne procedimientos ISO 9001 en Markdown.
* **keyword** (opcional) relaciona palabras clave con documentos (1\:N).
* **telegram\_update** registra toda interacción para auditoría.

Con este documento se puede recrear la base completa ejecutando el DDL en un servidor MySQL 8.2 limpio.
