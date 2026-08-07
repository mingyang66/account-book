-- 分类表
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- 分类唯一标识ID
    name TEXT NOT NULL,                          -- 分类名称
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),  -- 分类类型: income=收入, expense=支出
    icon TEXT DEFAULT '📁',                        -- 分类图标（Emoji）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 创建时间
);

-- 交易记录表
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- 交易唯一标识ID
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),  -- 交易类型: income=收入, expense=支出
    amount REAL NOT NULL,                        -- 交易金额
    category_id INTEGER,                         -- 所属分类ID，关联categories表
    note TEXT,                                   -- 交易备注
    date DATE NOT NULL,                          -- 交易日期（格式: YYYY-MM-DD）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    FOREIGN KEY (category_id) REFERENCES categories(id)  -- 外键约束，关联分类表
);
