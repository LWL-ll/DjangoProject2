## 目录说明

| 目录/文件 | 用途 |
|-----------|------|
| `DjangoProject2/` | 项目核心配置，包含路由、设置、WSGI/ASGI 入口 |
| `home/` | 首页模块，负责展示视差滚动效果和轮播图 |
| `lauth/` | 用户认证模块，处理登录、注册、会话管理 |
| `community/` | 社区模块，包含避雷墙和美食推荐功能 |
| `personalize/` | 个性化推荐模块，根据用户偏好推荐美食 |
| `static/` | 全局静态资源，存放第三方框架和公共图片 |
| `templates/` | 全局模板，存放公共组件如导航栏 |
| `my.cnf` | 云服务器 MySQL 连接配置 |
| `.gitignore` | 排除缓存、数据库、敏感配置等文件 |

## 技术栈

- **后端**：Django 6.0.4
- **数据库**：MySQL 5.7（云服务器）
- **前端**：HTML5 + CSS3 + JavaScript + Bootstrap 5
- **部署**：开发环境使用 Django 内置服务器，生产环境建议使用 Gunicorn/Nginx


