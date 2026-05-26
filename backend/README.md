# Backend MVP

这是 Boss Android MVP 的后端控制平面，当前职责是：

- 提供 FastAPI 接口
- 维护平台注册、设备、职位、模板、任务和执行记录
- 使用 SQLAlchemy 持久化数据
- 提供 Celery 任务入口
- 定义 Android Adapter 和 Driver 接口
- 跑一条模拟的 Boss Android 任务执行链路

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

- 已接入数据库模型和基础 CRUD API
- 默认可用 SQLite 本地启动
- `boss_android` 平台会在启动时自动初始化
- Celery 默认支持本地 eager 执行，方便先跑通链路
- 真实 Appium 点击和设备接入仍然需要继续实现
