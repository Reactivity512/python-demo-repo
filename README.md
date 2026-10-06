# python-demo-repo

Демо-репозиторий для DocScribe (агент автодокументации с HITL).

## Установка

```bash
pip install -e .
```

## Быстрый старт

```python
from demopkg import Client

client = Client(token="demo-token")
items = client.list_items(page_size=10)
print(items.total)
```
