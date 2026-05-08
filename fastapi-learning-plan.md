# FastAPI 从入门到精通 56 天学习计划

适合起点：已经学完 Python 基础语法，准备系统掌握 FastAPI，并最终能独立开发、测试和部署生产级 API。

建议节奏：每天 1.5-2.5 小时。

每日固定流程：

1. 20 分钟阅读文档或教程。
2. 60-90 分钟写代码。
3. 20 分钟补测试或调试。
4. 10 分钟写学习笔记。

官方资料：

- FastAPI Tutorial: <https://fastapi.tiangolo.com/tutorial/>
- Dependencies: <https://fastapi.tiangolo.com/tutorial/dependencies/>
- Testing: <https://fastapi.tiangolo.com/tutorial/testing/>
- SQL Databases: <https://fastapi.tiangolo.com/tutorial/sql-databases/>
- Security: <https://fastapi.tiangolo.com/tutorial/security/>
- Deployment: <https://fastapi.tiangolo.com/deployment/>

## 第 1 周：FastAPI 入门

目标：能启动 FastAPI 项目，理解路径参数、查询参数、请求体、响应模型和自动文档。

| 天数 | 学习内容 | 当天练习 |
| --- | --- | --- |
| Day 1 | 安装 FastAPI、虚拟环境、运行第一个接口 | 写 `/hello`，打开 `/docs` 查看接口文档 |
| Day 2 | HTTP 基础：GET、POST、PUT、DELETE、状态码 | 写 4 个不同 method 的接口 |
| Day 3 | 路径参数、查询参数、类型注解 | 写商品查询接口 |
| Day 4 | Request Body、Pydantic 模型 | 写创建商品接口 |
| Day 5 | Response Model、状态码、错误处理 | 写商品详情接口和 404 错误 |
| Day 6 | 内存版 CRUD | 完成 Todo API |
| Day 7 | 复盘和重构 | 整理 README 和接口文档 |

本周小项目：内存版 Todo API。

要求：

- 支持新增、查询、修改、删除 Todo。
- 使用 Pydantic 定义请求和响应模型。
- 能在 `/docs` 中清楚看到接口说明。

## 第 2 周：数据校验与接口设计

目标：熟练使用 Pydantic 和 FastAPI 的请求、响应、校验能力，写出更规范的接口。

| 天数 | 学习内容 | 当天练习 |
| --- | --- | --- |
| Day 8 | Pydantic v2：字段、默认值、`model_dump()` | 改造 Todo 模型 |
| Day 9 | 嵌套模型、列表、Enum、UUID、datetime | 写订单模型 |
| Day 10 | Header、Cookie、Form、File 上传 | 写头像上传接口 |
| Day 11 | OpenAPI 文档、tags、summary、description | 优化 `/docs` 展示 |
| Day 12 | 自定义校验、统一错误格式 | 写参数校验失败响应 |
| Day 13 | 分页、搜索、排序 | 商品列表支持分页 |
| Day 14 | 小项目整合 | 完成商品管理 API v1 |

本周小项目：商品管理 API。

要求：

- 支持商品创建、列表、详情、修改、删除。
- 支持分页、搜索、排序。
- 响应结构统一。
- 文档可读性良好。

## 第 3 周：依赖注入与项目结构

目标：理解 FastAPI 的依赖注入系统，并掌握中大型项目的基础目录组织方式。

| 天数 | 学习内容 | 当天练习 |
| --- | --- | --- |
| Day 15 | `Depends` 基础 | 抽出分页参数依赖 |
| Day 16 | 子依赖、`yield` 清理资源 | 模拟数据库连接依赖 |
| Day 17 | `APIRouter`、模块拆分 | 拆分 users/items routers |
| Day 18 | 配置管理、环境变量、`.env` | 写 settings 模块 |
| Day 19 | Middleware、CORS、请求日志 | 加请求耗时日志 |
| Day 20 | lifespan、启动和关闭事件 | 启动时初始化资源 |
| Day 21 | 重构日 | 把项目整理成标准结构 |

推荐项目结构：

```text
app/
  main.py
  core/
    config.py
  api/
    routes/
      users.py
      items.py
  schemas/
  services/
  repositories/
  tests/
```

本周小项目：结构化商品管理 API。

要求：

- 使用 `APIRouter` 拆分接口。
- 使用 settings 管理配置。
- 使用依赖注入复用分页、配置和资源。

## 第 4 周：数据库

目标：掌握 FastAPI 与数据库结合的方式，理解 ORM、Session、迁移和事务。

| 天数 | 学习内容 | 当天练习 |
| --- | --- | --- |
| Day 22 | SQL 基础、SQLite/PostgreSQL 概念 | 设计 3 张表 |
| Day 23 | SQLModel/SQLAlchemy、Session、CRUD | Todo 入库 |
| Day 24 | 表关系、一对多、多对多 | 用户和文章关系 |
| Day 25 | Alembic 数据库迁移 | 新增字段并迁移 |
| Day 26 | 事务、Repository/Service 分层 | 抽出 service 层 |
| Day 27 | 数据库测试、测试库隔离 | 写 CRUD 测试 |
| Day 28 | 小项目整合 | 完成博客 API：用户、文章、评论 |

本周小项目：博客 API。

要求：

- 用户、文章、评论三类资源。
- 文章属于用户，评论属于文章。
- 使用数据库持久化。
- 使用迁移管理表结构变化。

## 第 5 周：认证与安全

目标：掌握注册、登录、密码哈希、JWT、权限控制和常见安全配置。

| 天数 | 学习内容 | 当天练习 |
| --- | --- | --- |
| Day 29 | 密码哈希、注册和登录流程 | 注册和登录接口 |
| Day 30 | OAuth2、JWT、Bearer Token | 返回 access token |
| Day 31 | 当前用户依赖、权限控制 | `/me` 和管理员接口 |
| Day 32 | 角色、权限、接口保护 | 普通用户和管理员分权 |
| Day 33 | CORS、安全响应、限流概念 | 加基础安全配置 |
| Day 34 | 文件上传、后台任务 | 上传文件后后台处理 |
| Day 35 | 小项目整合 | 完成带登录的博客 API |

本周小项目：带认证的博客 API。

要求：

- 支持注册、登录、获取当前用户。
- 使用 JWT 保护接口。
- 作者只能修改自己的文章。
- 管理员可以删除任意评论。

## 第 6 周：测试与工程质量

目标：建立测试习惯，能为接口、认证、数据库和异常场景写可靠测试。

| 天数 | 学习内容 | 当天练习 |
| --- | --- | --- |
| Day 36 | pytest、FastAPI `TestClient` | 测 5 个接口 |
| Day 37 | `dependency_overrides` | 替换数据库依赖 |
| Day 38 | 异步测试、HTTPX | 测 async 接口 |
| Day 39 | 测认证、异常、边界参数 | 覆盖登录失败场景 |
| Day 40 | ruff、mypy、pre-commit | 加代码质量检查 |
| Day 41 | 日志、异常追踪、统一响应 | 加结构化日志 |
| Day 42 | 项目加固 | 测试覆盖率达到 70% 以上 |

本周小项目：给博客 API 补测试。

要求：

- 覆盖注册、登录、文章 CRUD、权限失败场景。
- 测试数据库隔离。
- 增加 lint 和格式化检查。

## 第 7 周：进阶架构与性能

目标：理解异步、缓存、后台任务、版本管理、分层架构和基本性能优化。

| 天数 | 学习内容 | 当天练习 |
| --- | --- | --- |
| Day 43 | async/sync 区别、I/O 密集场景 | 改造外部请求接口 |
| Day 44 | Redis 缓存、过期时间、缓存失效 | 给列表接口加缓存 |
| Day 45 | 后台任务队列：Celery/RQ/Arq 概念 | 模拟发送邮件任务 |
| Day 46 | API 版本管理、分页规范、错误规范 | 做 `/api/v1` 结构 |
| Day 47 | 分层架构：router/service/repository/schema | 重构博客项目 |
| Day 48 | 超时、重试、连接池 | 给外部 API 加 timeout |
| Day 49 | 压测入门、性能观察 | 用简单压测找瓶颈 |

本周小项目：进阶版任务系统 API。

要求：

- 用户、项目、任务、评论。
- 使用 Redis 缓存常用列表。
- 使用后台任务模拟通知。
- 明确分层结构。

## 第 8 周：部署与毕业项目

目标：掌握 Docker、Compose、生产启动方式、健康检查、CI/CD 和部署注意事项。

| 天数 | 学习内容 | 当天练习 |
| --- | --- | --- |
| Day 50 | Dockerfile、镜像构建 | 容器运行 FastAPI |
| Day 51 | Docker Compose + PostgreSQL | 本地一键启动 |
| Day 52 | 部署概念：HTTPS、重启、workers、内存 | 写部署 checklist |
| Day 53 | Uvicorn/FastAPI run、反向代理概念 | 配生产启动命令 |
| Day 54 | CI/CD：测试、lint、构建镜像 | 写 GitHub Actions |
| Day 55 | 健康检查、日志、监控、Sentry 概念 | 加 `/health` |
| Day 56 | 毕业项目交付 | 部署一个完整 API |

毕业项目：任务协作系统 API。

核心功能：

- 用户注册、登录、JWT 认证。
- 项目管理。
- 任务管理。
- 评论系统。
- 附件上传。
- 权限控制。
- 分页、搜索、排序。
- PostgreSQL 持久化。
- Redis 缓存。
- 后台通知任务。
- pytest 测试。
- Docker Compose 一键启动。
- `/health` 健康检查接口。

## 学习完成标准

学完后你应该能做到：

- 独立创建 FastAPI 项目。
- 熟练定义请求参数、响应模型和错误处理。
- 使用依赖注入组织公共逻辑。
- 使用数据库完成真实 CRUD。
- 实现注册、登录、JWT 认证和权限控制。
- 编写接口测试和数据库测试。
- 使用 Docker 部署 FastAPI 服务。
- 读懂大部分 FastAPI 项目结构。
- 能独立开发一个中小型后端 API。

## 建议补充知识

FastAPI 学到中后期，建议同步补这些内容：

- HTTP 协议基础。
- RESTful API 设计。
- SQL 和 PostgreSQL。
- pytest 测试框架。
- Docker 和 Docker Compose。
- Linux 基础命令。
- Git 分支和 Pull Request 工作流。
- 基础安全知识：密码哈希、Token、CORS、HTTPS。

## 每周复盘模板

每周结束后写一次复盘：

```md
## 本周学了什么

- 

## 本周完成的代码

- 

## 还不理解的问题

- 

## 下周要重点突破

- 
```

