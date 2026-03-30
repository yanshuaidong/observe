## strategy表说明
```sql
CREATE TABLE IF NOT EXISTS strategy (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  strategyid VARCHAR(64) NOT NULL,
  content JSON NOT NULL,
  UNIQUE KEY uk_strategy_strategyid (strategyid)
);
```

## content 约定（Blob-first）
- 后端不解析 `content` 内部结构，只负责保存/读取整份 JSON。
- 前端负责在 `content` 里维护“策略名字/说明/考虑方面/执行情况/每日记录...等”字段结构；
