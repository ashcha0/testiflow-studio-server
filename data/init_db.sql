-- 数据库初始化脚本
-- 创建outlines表
CREATE TABLE IF NOT EXISTS outlines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- 创建outline_sections表
CREATE TABLE IF NOT EXISTS outline_sections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    outline_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    FOREIGN KEY (outline_id) REFERENCES outlines(id) ON DELETE CASCADE
);

-- 创建scripts表
CREATE TABLE IF NOT EXISTS scripts (
    id VARCHAR(36) PRIMARY KEY,
    outline_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (outline_id) REFERENCES outlines(id) ON DELETE CASCADE
);