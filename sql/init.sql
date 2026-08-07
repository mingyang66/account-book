-- 账号表
CREATE TABLE IF NOT EXISTS my_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- 账号唯一标识ID
    username TEXT NOT NULL UNIQUE,               -- 用户名
    password TEXT NOT NULL,                      -- 密码
    createTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP   -- 更新时间
);

-- 分类表
CREATE TABLE IF NOT EXISTS my_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- 分类唯一标识ID
    name TEXT NOT NULL,                          -- 分类名称
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),  -- 分类类型: income=收入, expense=支出
    icon TEXT DEFAULT '📁',                        -- 分类图标（Emoji）
    createTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP   -- 更新时间
);

-- 交易记录表
CREATE TABLE IF NOT EXISTS my_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- 交易唯一标识ID
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),  -- 交易类型: income=收入, expense=支出
    amount REAL NOT NULL,                        -- 交易金额
    category_id INTEGER,                         -- 所属分类ID，关联categories表
    note TEXT,                                   -- 交易备注
    date DATE NOT NULL,                          -- 交易日期（格式: YYYY-MM-DD）
    createTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 更新时间
    FOREIGN KEY (category_id) REFERENCES my_categories(id)  -- 外键约束，关联分类表
);
