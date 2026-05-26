# Backend MVP

这是 Boss Android MVP 的后端骨架，当前职责是：

- 提供 FastAPI 接口
- 维护平台注册信息
- 维护任务状态
- 提供 Celery 任务入口
- 定义 Android Adapter 和 Driver 接口

## 运行方式

安装依赖后可启动：

```bash
uvicorn app.main:app --reload
```

启动 Celery worker：

```bash
celery -A app.workers.celery_app:celery_app worker --loglevel=info
```

## 当前状态

这是一个可继续开发的骨架，不包含真实数据库落库和真实 Appium 操作实现。

