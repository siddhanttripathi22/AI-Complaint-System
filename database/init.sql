CREATE DATABASE IF NOT EXISTS complaints_db;
USE complaints_db;

CREATE TABLE IF NOT EXISTS complaints (
    id                  INT AUTO_INCREMENT PRIMARY KEY,

    
    complaint_source    VARCHAR(255),
    customer_name       VARCHAR(255),

    
    product_name        VARCHAR(255),
    product_strength    VARCHAR(255),
    batch_number        VARCHAR(255),
    manufacturing_date  VARCHAR(100),
    expiry_date         VARCHAR(100),
    quantity_affected   VARCHAR(100),

    
    complaint_type      VARCHAR(255),
    complaint_date      VARCHAR(100),
    description         TEXT,

   
    initial_severity    VARCHAR(100),
    priority            VARCHAR(100),

   
    ai_summary          TEXT,
    ai_risk             VARCHAR(100),

    status              VARCHAR(50) DEFAULT 'Pending Triage',
    created_at          DATETIME    DEFAULT CURRENT_TIMESTAMP
);
