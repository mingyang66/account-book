-- 账号表
CREATE TABLE IF NOT EXISTS my_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- 账号唯一标识ID
    accountcode INTEGER NOT NULL UNIQUE,          -- 账号唯一编号
    username TEXT NOT NULL UNIQUE,               -- 用户名
    password TEXT NOT NULL,                      -- 密码
    createTime TIMESTAMP DEFAULT (datetime('now', '+8 hours')),  -- UTC+8创建时间
    updateTime TIMESTAMP DEFAULT (datetime('now', '+8 hours'))   -- UTC+8更新时间
);

-- 分类表
CREATE TABLE IF NOT EXISTS my_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- 分类唯一标识ID
    name TEXT NOT NULL,                          -- 分类名称
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),  -- 分类类型: income=收入, expense=支出
    icon TEXT DEFAULT '📁',                        -- 分类图标（Emoji）
    createTime TIMESTAMP DEFAULT (datetime('now', '+8 hours')),  -- UTC+8创建时间
    updateTime TIMESTAMP DEFAULT (datetime('now', '+8 hours'))   -- UTC+8更新时间
);

-- 交易记录表
CREATE TABLE IF NOT EXISTS my_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- 交易唯一标识ID
    accountcode INTEGER NOT NULL,                 -- 所属账号唯一编号
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),  -- 交易类型: income=收入, expense=支出
    amount REAL NOT NULL,                        -- 交易金额
    category_id INTEGER,                         -- 所属分类ID，关联categories表
    note TEXT,                                   -- 交易备注
    date DATE NOT NULL,                          -- 交易日期（格式: YYYY-MM-DD）
    createTime TIMESTAMP DEFAULT (datetime('now', '+8 hours')),  -- UTC+8创建时间
    updateTime TIMESTAMP DEFAULT (datetime('now', '+8 hours')),  -- UTC+8更新时间
    FOREIGN KEY (category_id) REFERENCES my_categories(id), -- 外键约束，关联分类表
    FOREIGN KEY (accountcode) REFERENCES my_account(accountcode) -- 外键约束，关联账号表
);

CREATE INDEX IF NOT EXISTS idx_transactions_account_date
ON my_transactions(accountcode, date);

-- 记事本表
CREATE TABLE IF NOT EXISTS my_notebooks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- 记事本唯一标识ID
    accountcode INTEGER NOT NULL,                -- 所属账号唯一编号
    title TEXT NOT NULL CHECK(length(title) <= 64), -- 记事本标题，最多64个字符
    content TEXT NOT NULL DEFAULT '',            -- 记事本正文
    createTime TIMESTAMP DEFAULT (datetime('now', '+8 hours')),  -- UTC+8创建时间
    updateTime TIMESTAMP DEFAULT (datetime('now', '+8 hours')),  -- UTC+8更新时间
    FOREIGN KEY (accountcode) REFERENCES my_account(accountcode) -- 外键约束，关联账号表
);

CREATE INDEX IF NOT EXISTS idx_notebooks_account_created_updated
ON my_notebooks(accountcode, date(createTime) DESC, updateTime DESC);
