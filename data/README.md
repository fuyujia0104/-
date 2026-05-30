# 数据目录

本目录包含城市感官探索家项目的数据文件。

## 文件说明

### sensory_marks.db
SQLite数据库文件，存储用户的感官标记数据。

数据库包含以下表：

1. `marks` - 存储用户的感官标记
   - `id`: 标记ID（主键）
   - `lat`: 纬度
   - `lon`: 经度
   - `mark`: 标记内容
   - `type`: 标记类型
   - `created_at`: 创建时间

2. `locations` - 存储位置信息
   - `id`: 位置ID（主键）
   - `address`: 地址
   - `latitude`: 纬度
   - `longitude`: 经度
   - `created_at`: 创建时间
   - `updated_at`: 更新时间

## 数据库初始化

数据库文件会在首次运行应用时自动创建。如果需要重新初始化数据库，可以删除现有的`sensory_marks.db`文件，然后重新运行应用。

## 数据备份

建议定期备份数据库文件，以防止数据丢失。可以使用以下方法备份：

1. 直接复制数据库文件
2. 使用SQLite的备份命令：
```bash
sqlite3 sensory_marks.db ".backup sensory_marks_backup.db"
```

## 数据恢复

如果需要恢复数据库，可以使用以下方法：

1. 直接替换数据库文件
2. 使用SQLite的恢复命令：
```bash
sqlite3 sensory_marks.db ".restore sensory_marks_backup.db"
```

注意：在恢复数据库之前，建议先备份当前的数据库文件。
