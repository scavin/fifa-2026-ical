# FIFA World Cup 2026 ICS 中文化

当前目录保留一个版本：

- `translate_fifa_ics.py`
  只用 Python 标准库。自己处理 ICS unfold/fold，再按字段翻译。

## 用法

```bash
python3 translate_fifa_ics.py -o fifa-world-cup-2026.zh.ics
```

## 特点

- 无第三方依赖，适合 cron 和最小部署。
- 对当前 `fixtur.es` 这类结构简单的源足够稳。
- 尽量保留原始文件格式，不会因为库序列化而重排太多内容。

## 取舍

- 无第三方依赖，适合 cron 和最小部署。
- 对当前 `fixtur.es` 这类结构简单的源足够稳。
- 尽量保留原始文件格式，不会因为库序列化而重排太多内容。

- 你自己维护 ICS 细节兼容性。
- 如果未来源变复杂，维护成本会上升。
