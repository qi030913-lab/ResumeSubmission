# API 设计

## 1. 设计原则

第一版 API 不追求“大而全”，重点覆盖：

- 平台与设备可见
- 简历与模板可管理
- Boss Android 沟通任务可创建
- 任务状态可查询
- 失败可回看

接口统一前缀建议：

- `/api/v1`

---

## 2. 健康检查

### `GET /api/v1/health`

用途：

- 存活检查

响应示例：

```json
{
  "status": "ok",
  "service": "resume-automation-api"
}
```

### `GET /api/v1/ready`

用途：

- 就绪检查

---

## 3. 平台相关

### `GET /api/v1/platforms`

用途：

- 获取已注册平台列表

响应字段建议：

- `platform_code`
- `platform_name`
- `platform_type`
- `health_status`
- `supported_actions`

### `GET /api/v1/platforms/{platform_code}`

用途：

- 查看单个平台详情

### `POST /api/v1/platforms`

用途：

- 新增平台注册记录

请求示例：

```json
{
  "platform_code": "boss_android",
  "platform_name": "Boss 直聘 Android",
  "platform_family": "boss",
  "platform_type": "android_app",
  "adapter_code": "boss_android_adapter"
}
```

---

## 4. 设备相关

### `GET /api/v1/devices`

用途：

- 获取可用设备列表

### `POST /api/v1/devices`

用途：

- 注册 Android 设备或网页执行节点

请求示例：

```json
{
  "device_code": "pixel7-local",
  "platform_type": "android_app",
  "device_name": "Pixel 7",
  "adb_serial": "emulator-5554"
}
```

---

## 5. 简历档案相关

### `GET /api/v1/profiles`

### `POST /api/v1/profiles`

### `GET /api/v1/profiles/{profile_id}`

### `POST /api/v1/profiles/{profile_id}/assets`

用途：

- 管理结构化简历档案与附件

---

## 6. 消息模板相关

### `GET /api/v1/message-templates`

用途：

- 列出首句模板

可选筛选：

- `platform_code`
- `scene_code`

### `POST /api/v1/message-templates`

请求示例：

```json
{
  "platform_code": "boss_android",
  "scene_code": "start_chat",
  "title": "Java 岗位首句",
  "template_text": "Boss您好，我对您发布的{{job_title}}岗位很感兴趣，可以把简历发给您吗？最快可以{{availability_date}}左右到岗。"
}
```

---

## 7. 职位相关

### `POST /api/v1/jobs`

用途：

- 手工或自动写入职位快照

### `GET /api/v1/jobs`

用途：

- 查询职位列表

可选筛选：

- `platform_code`
- `company_name`
- `city`

---

## 8. 任务相关

### `POST /api/v1/tasks`

用途：

- 创建执行任务

第一版重点支持：

- `start_chat`
- `send_resume`

请求示例：

```json
{
  "platform_code": "boss_android",
  "platform_type": "android_app",
  "action_type": "start_chat",
  "job_id": "7ee67065-6ee5-4f07-9b1a-3cb363ab698f",
  "device_id": "9d0bc81d-38b4-4eb9-8499-c8b89fbcbd9c",
  "profile_id": "20ff8d18-849b-40a8-b99d-f0d27c65ea0e",
  "message_template_id": "b22bc26c-7030-4ce3-bf39-fc684a1f6bb8",
  "requires_manual_review": true,
  "payload": {
    "send_greeting": true
  }
}
```

响应示例：

```json
{
  "id": "c7e8b267-7083-442a-9a5d-9b79e5b8badd",
  "status": "queued",
  "platform_code": "boss_android",
  "action_type": "start_chat"
}
```

### `GET /api/v1/tasks`

用途：

- 查询任务列表

筛选建议：

- `status`
- `platform_code`
- `action_type`

### `GET /api/v1/tasks/{task_id}`

用途：

- 查询单个任务详情

### `POST /api/v1/tasks/{task_id}/dispatch`

用途：

- 主动下发任务到 Celery

### `PATCH /api/v1/tasks/{task_id}/status`

用途：

- 更新任务状态

### `POST /api/v1/tasks/{task_id}/retry`

用途：

- 重试失败任务

---

## 9. 执行记录相关

### `GET /api/v1/runs`

用途：

- 查询执行记录

### `GET /api/v1/tasks/{task_id}/runs`

用途：

- 查看某任务的执行历史

### `GET /api/v1/runs/{run_id}`

用途：

- 查看单次执行详情、截图、错误

---

## 10. 人工审核相关

### `GET /api/v1/manual-reviews`

### `POST /api/v1/manual-reviews/{review_id}/approve`

### `POST /api/v1/manual-reviews/{review_id}/reject`

用途：

- 处理验证码、风险弹窗、低置信度发送等场景

---

## 11. Boss Android MVP 的最小 API 集

第一阶段你真要开工，先做下面这些就够：

- `GET /api/v1/health`
- `GET /api/v1/platforms`
- `GET /api/v1/devices`
- `POST /api/v1/tasks`
- `GET /api/v1/tasks`
- `GET /api/v1/tasks/{task_id}`
- `POST /api/v1/tasks/{task_id}/dispatch`
- `PATCH /api/v1/tasks/{task_id}/status`

---

## 12. 状态码约定

### 任务状态

- `draft`
- `queued`
- `running`
- `waiting_manual_review`
- `succeeded`
- `failed`
- `blocked`
- `skipped_duplicate`

### 错误码建议

- `PLATFORM_NOT_SUPPORTED`
- `DEVICE_OFFLINE`
- `ELEMENT_NOT_FOUND`
- `RISK_PROMPT_DETECTED`
- `DUPLICATE_CONTACT`
- `MANUAL_REVIEW_REQUIRED`

