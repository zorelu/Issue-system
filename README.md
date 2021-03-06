# v1.0 stable

## [python 虚拟环境](https://www.jianshu.com/p/08c657bd34f1)

## 环境依赖

- python 3.4+
- mysql or mssql

## 部署步骤

1. 安装项目依赖的包

```bash
    pip install -r requirements.txt
```

2. 到项目中对数据库进行创建并对应于 config.py 文件

3. 到项目中执行脚本 如果是新装要执行

- python manage.py db init

- python manage.py db migrate

- python manage.py db upgrade

- 创建数据库

4. 启动项目

```bash
    python blog.py
```

## 目录结构描述

```
├── Readme.md  // help
├── blog.py    // 应用
├── config.py  // 配置
├── models.py  // 数据库模型
├── manage.py  // 数据库更新创建脚本
├── static     // web静态资源加载
│   └── css    // css 文件
│   └── images // images文件
├── templates  // html页面
│   └── base   // 基础模板
```

## V1.0.0 版本内容更新

1. 用户登录注册功能
2. 问题发布功能
3. 个人中心功能（由头像点击进去）
4. 个人头像上传功能


## 下面是路由的 demo

```py
@app.route('/')

@app.route('/<int:page>',methods=['GET', 'POST'])
```

## 首页路由

```py
# 获取 get 请求传过来的页数,没有传参数，默认为 1
def index(page=None)

# 获取 get 请求传过来的以多少条数据分页的参数，默认为 5
page = int(request.args.get('page', 1))

# 按时间排序 -号
per_page = int(request.args.get('per_page', 5))

# 获得数据
page = Question.query.order_by('-create_time').paginate(page, per_page, error_out=False) # print(page)

context = {
    'questions' :page.items
    #'questions' : Question.query.order_by('-create_time').all()
}

# 传值
return render_template('index.html',page=page,\*\*context)
```
