# Web Framework
![project_license](https://badgen.net/badge/License/GPL-3.0/green)
![python_depend](https://badgen.net/badge/Python/3.7.9+/blue)
![mysql_depend](https://badgen.net/badge/MySQL/5.7/orange)

一个使用 `Python` 基于 `socket` 开发的 `MVC` 架构的 Web 框架。
***
![socket](/screenshot/socket.gif)
***
## 项目介绍
- 基于 `socket` 实现多线程的 Web 服务器的构建。
- 采用 `MVC` 架构，减少系统耦合，提高系统灵活性以及代码可重用性。
- 实现对 `HTTP` 请求的解析以及 `HTTP` 响应的生成。
- 实现 `session` 的生成并分发在 `HTTP` 响应的 `Cookie` 中以维持客户端与服务端之间的连接状态。 
- 实现对 `HTTP` 请求中的 `Cookie` 内的 `session` 在服务端的验证。
- 使用 `Jinja2` 作为模板引擎，完成前端页面的生成。
- 使用原生 `JavaScript` 实现 `AJAX` 应用的封装。
- 实现对 `CSRF` 及 `XSS` 攻击的防御：
  - 通过生成摘要、加盐等方法生成可进行过期时间验证的 `CSRF Token` 并分发在表单中。
  - 实现服务端对 `CSRF Token` 的验证。
  - 通过 `Jinja2` 对静态 `HTML` 内容的自动转义以应对 `XSS` 攻击。
  - 使用原生 `JavaScript` 实现对动态内容的转义以应对 `XSS` 攻击。
- 基于 `PyMySQL` 实现了适配 `MySQL` 的轻量级 `ORM`。
- 实现了完整的用户系统，包括用户登录，注册，鉴权等功能。
- 基于用户系统实现了 Todo 功能，包括用户对 Todo 内容的查看、发布、修改和删除。
- 实现了 Todo 相关功能的 `API` 接口，以及实现了相关 `API` 的鉴权。
- 基于 Todo 相关功能的 `API` 接口，实现了基于 `AJAX` 应用的 Todo 功能。