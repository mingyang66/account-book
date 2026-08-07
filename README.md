# 记账本 - 个人财务管理

基于 Python + PySide6 开发的桌面端个人记账应用，支持收支记录、分类管理和数据统计。

## 功能特性

- **仪表盘概览** - 快速查看总收入、总支出、结余及分类占比
- **收支记录** - 添加、编辑、删除交易记录，支持备注和日期选择
- **分类管理** - 自定义收入和支出分类，支持 Emoji 图标
- **数据统计** - 按月度、年度汇总收支，支持图表化分析
- **筛选过滤** - 按日期范围、类型、分类等多维度筛选记录

## 技术栈

| 组件 | 说明 |
|------|------|
| Python 3.8+ | 运行环境 |
| PySide6 | GUI 框架 |
| SQLite | 本地数据库 |
| PyInstaller | 打包工具 |

## 项目结构

```
account-book/
├── main.py              # 程序入口
├── database.py          # 数据库操作类
├── styles.py            # 界面样式（QSS）
├── requirements.txt     # Python 依赖
├── sql/
│   └── init.sql         # 数据库初始化脚本
├── ui/
│   ├── main_window.py   # 主窗口
│   └── dialogs.py       # 对话框
└── assets/              # 静态资源（图标等）
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python main.py
```

## 打包发布

使用 PyInstaller 打包为 Windows 可执行程序：

```bash
python -m PyInstaller --noconsole --onefile --add-data "ui;ui" --add-data "sql;sql" --name "AccountBook" main.py
```

打包完成后，可执行文件位于 `dist/AccountBook.exe`。

## 使用说明

### 添加记录
1. 点击左侧菜单 **收支记录**
2. 点击右上角 **新增** 按钮
3. 选择类型（收入/支出）、分类，填写金额和备注
4. 点击 **保存**

### 分类管理
- 进入 **分类管理** 页面
- 点击 **新增分类** 添加自定义分类
- 设置分类名称和 Emoji 图标

### 数据统计
- 进入 **数据统计** 页面
- 选择日期范围
- 查看月度收支汇总和分类占比

## 数据库

使用 SQLite 本地数据库（`account_book.db`），首次运行自动创建。

- **categories** - 分类表
- **transactions** - 交易记录表

数据库初始化脚本：`sql/init.sql`

## License

MIT
