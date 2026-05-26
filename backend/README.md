# Backend MVP

这是 Boss Android MVP 的后端控制平面，当前职责是：

- 提供 FastAPI 接口
- 维护平台注册、设备、职位、模板、任务和执行记录
- 使用 SQLAlchemy 持久化数据
- 提供 Celery 任务入口
- 定义 Android Adapter 和 Driver 接口
- 支持 `mock` / `appium` 两种 Android driver 模式
- 跑一条 Boss Android 任务执行链路

## 运行方式

安装依赖后可启动：

```bash
uvicorn app.main:app --reload
```

启动 Celery worker：

```bash
celery -A app.workers.celery_app:celery_app worker --loglevel=info
```

## 数据库迁移

执行初始迁移：

```bash
alembic -c alembic.ini upgrade head
```

## PostgreSQL / Redis 本地服务

```bash
docker compose -f docker-compose.services.yml up -d
```

建议 `.env` 配置：

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/resume_automation
DATABASE_AUTO_CREATE=false
DATABASE_SEED_REFERENCE_DATA=true
```

## Appium + ADB 模式

默认是 `mock` 模式。切到真机模式时，准备：

1. 启动 Appium Server
2. 安装 `uiautomator2` driver
3. 确保 `adb devices` 能看到设备
4. 在 `.env` 中设置：

```env
ANDROID_DRIVER_MODE=appium
ANDROID_ADB_PATH=adb
ANDROID_DEFAULT_DEVICE_SERIAL=<your-device-serial>
ANDROID_ARTIFACTS_DIR=./artifacts
APPIUM_SERVER_URL=http://127.0.0.1:4723
APPIUM_PLATFORM_NAME=Android
APPIUM_AUTOMATION_NAME=UiAutomator2
APPIUM_DEVICE_NAME=Android
APPIUM_NO_RESET=true
APPIUM_APP_PACKAGE=
APPIUM_APP_ACTIVITY=
```

如果 `APPIUM_APP_PACKAGE` / `APPIUM_APP_ACTIVITY` 留空，当前默认假定 App 已经在前台。

## 当前状态

- 已接入数据库模型和基础 CRUD API
- 默认可用 SQLite 本地启动
- `boss_android` 平台会在启动时自动初始化
- Celery 默认支持本地 eager 执行，方便先跑通链路
- 已补 `Appium + ADB` 真机 driver 结构
- Boss `start_chat` 默认只点击 `立即沟通`，利用 App 自动发送常用短语
- 真实 Boss 元素定位和选择器仍然需要继续采集
