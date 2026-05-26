# ResumeSubmission

一个面向 **招聘网站 + 招聘 App** 的自动沟通与投递项目，当前重点是 **Boss 直聘 Android App** 的 MVP 链路：

1. 进入职位详情
2. 点击 `立即沟通`
3. 自动发送首句
4. 记录任务状态和执行结果

这个仓库现在不是成品，但已经不是空骨架了：架构文档、数据设计、API 设计、数据库模型、后端控制平面、Celery 任务入口，以及一条可执行的 Boss Android 模拟任务链路都已经落地。

## 项目目标

项目最终想解决的不是单一网页“投简历”问题，而是统一处理这些动作：

- 打开职位
- 发起沟通
- 发送首句
- 发送简历
- 提交申请
- 去重与频控
- 人工审核与失败回放

为了支持后续增加智联、拉勾、前程无忧等平台，仓库按 **控制平面 + 多端执行器 + 平台适配器** 的方式设计。

## 当前状态

已完成：

- Python 技术路线定稿
- Boss Android 场景的整体架构文档
- 项目目录结构设计
- 数据库表设计草案
- API 设计草案
- SQLAlchemy 数据模型和 SQLite / PostgreSQL 配置
- FastAPI CRUD API
- Celery worker 入口和本地 eager 执行
- Boss Android adapter / `mock` / `appium` 双驱动结构
- 任务执行记录、去重记录、执行日志落库
- Alembic 初始迁移
- 基础测试通过

暂未完成：

- 真实 Boss `立即沟通` 点击链路
- 截图归档、回放、风控识别

## 仓库结构

```text
.
├── README.md
├── 自动投递简历系统技术方案.md
├── docs/
│   ├── 01-项目目录结构.md
│   ├── 02-数据库表设计.md
│   ├── 03-API设计.md
│   └── 04-Boss-Android-MVP实施清单.md
└── backend/
    ├── pyproject.toml
    ├── .env.example
    ├── README.md
    ├── app/
    │   ├── main.py
    │   ├── api/
    │   ├── core/
    │   ├── schemas/
    │   ├── services/
    │   ├── adapters/
    │   ├── drivers/
    │   └── workers/
    └── tests/
```

## 技术栈

- 后端控制平面：`Python 3.11+`、`FastAPI`
- 数据建模：`Pydantic v2`
- ORM / 迁移：`SQLAlchemy 2`、`Alembic`
- 异步任务：`Celery`、`Redis`
- 网页执行器：`Playwright Python`
- Android 执行器：`Appium Python Client`、`UiAutomator2`、`ADB`
- 数据库：`PostgreSQL`

## 核心设计

### 1. Driver 和 Adapter 分层

- `driver` 负责底层动作：点击、输入、截图、滑动
- `adapter` 负责平台业务：哪里是 `立即沟通`、何时算成功、异常怎么处理

这样后面接别的平台时，不需要重写整个调度流程。

### 2. 统一动作抽象

不同平台按钮名字不同，但上层统一抽象为：

- `open_job`
- `start_chat`
- `send_greeting`
- `send_resume`
- `submit_application`

### 3. 多平台扩展优先

当前先做 Boss Android，但模型已经预留：

- `platform_registry`
- `platform_capabilities`
- `dedupe_records`
- `platform_code + platform_type`

这让后续接网页端和其他 App 时不需要推倒重来。

## 快速开始

### 1. 进入后端目录

```bash
cd backend
```

### 2. 创建虚拟环境并安装依赖

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -e .[dev]
```

### 3. 配置环境变量

```bash
copy .env.example .env
```

按实际情况修改：

- `DATABASE_URL`
- `DATABASE_AUTO_CREATE`
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `ANDROID_DRIVER_MODE`
- `APPIUM_SERVER_URL`

### 4. 执行数据库迁移

```bash
alembic -c alembic.ini upgrade head
```

### 5. 启动 API

```bash
uvicorn app.main:app --reload
```

默认地址：

- API: `http://127.0.0.1:8000`
- OpenAPI: `http://127.0.0.1:8000/docs`

### 6. 启动 Celery Worker

```bash
celery -A app.workers.celery_app:celery_app worker --loglevel=info
```

### 7. 本地 PostgreSQL / Redis

```bash
docker compose -f docker-compose.services.yml up -d
```

## 当前可用接口

当前已经有一版可用接口：

- `GET /api/v1/health`
- `GET /api/v1/ready`
- `GET /api/v1/platforms`
- `GET /api/v1/platforms/{platform_code}`
- `POST /api/v1/platforms`
- `GET /api/v1/devices`
- `POST /api/v1/devices`
- `GET /api/v1/profiles`
- `POST /api/v1/profiles`
- `GET /api/v1/jobs`
- `POST /api/v1/jobs`
- `GET /api/v1/message-templates`
- `POST /api/v1/message-templates`
- `GET /api/v1/tasks`
- `GET /api/v1/tasks/{task_id}`
- `POST /api/v1/tasks`
- `POST /api/v1/tasks/{task_id}/dispatch`
- `PATCH /api/v1/tasks/{task_id}/status`
- `GET /api/v1/runs`
- `GET /api/v1/runs/{run_id}`

注意：当前数据已经是**数据库持久化**，默认本地使用 SQLite；生产化时建议切到 PostgreSQL。

## Boss Android MVP 路线

第一阶段只做最短闭环：

1. 识别职位详情页
2. 识别并点击 `立即沟通`
3. 进入聊天页
4. 输入并发送首句
5. 把结果回传到任务状态

建议开发顺序：

1. 把 `boss_android_adapter.py` 里的通用点击换成真实 Boss 选择器
2. 增加截图归档和失败回放
3. 增加风控识别和人工审核流
4. 把 SQLite 开发模式和 PostgreSQL 部署模式进一步拆清
5. 增加实际 Appium 集成测试

## 相关文档

- 总方案：[自动投递简历系统技术方案.md](./自动投递简历系统技术方案.md)
- 目录设计：[docs/01-项目目录结构.md](./docs/01-项目目录结构.md)
- 数据库设计：[docs/02-数据库表设计.md](./docs/02-数据库表设计.md)
- API 设计：[docs/03-API设计.md](./docs/03-API设计.md)
- Boss MVP 清单：[docs/04-Boss-Android-MVP实施清单.md](./docs/04-Boss-Android-MVP实施清单.md)
- 后端说明：[backend/README.md](./backend/README.md)

## 注意事项

- 这个项目当前只适合作为开发中的自动化骨架，不适合直接生产使用
- 不建议一上来就做高频海投
- 验证码、风控、异常弹窗必须预留人工介入
- 涉及平台账号、简历、手机号等敏感信息时，需要单独补安全策略

## 下一步

最值得立刻继续的两块：

- 采集 Boss 直聘真实元素选择器并接入 `Appium + ADB`
- 增加 PostgreSQL + Alembic 的正式部署说明
