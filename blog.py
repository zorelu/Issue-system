from flask import Flask,render_template,request,redirect,url_for,session
from loginreq import login_req
import config
from werkzeug.utils import secure_filename
import os
from exts import db
from models import User,Question
from datetime import timedelta
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
@app.route('/<int:page>',methods=['GET', 'POST'])

#首页路由
def index(page=None):
  # 获取get请求传过来的页数,没有传参数，默认为1
  page = int(request.args.get('page', 1))
  # 获取get请求传过来的以多少条数据分页的参数，默认为5
  per_page = int(request.args.get('per_page', 5))

  ###按时间排序 -号
  page = Question.query.order_by('-create_time').paginate(page, per_page, error_out=False)
  # print(page)
  # 获得数据
  context = {
    'questions' :page.items
    # 'questions' : Question.query.order_by('-create_time').all()
  }
  ###获取文章用户头像
  # b = page.items
  for getimg in page.items:
    userimg = User.query.filter(getimg.author_id == User.id).first()
    # print (img1.img_url)

  return render_template('index.html',userimg=userimg,page=page,**context)

@app.route('/regist/', methods=['GET', 'POST'])
#注册路由
def regist():
  # remove the username from the session if it's there
  if request.method == 'GET':
    return render_template('regist.html')
  else:
    telephone = request.form['telephone']
    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']
    img_url =  'default.jpg'
    #判断手机号是否存在重复
    user = User.query.filter(User.telephone == telephone).first()
    if user:
      return '手机号码已经被注册'
    else:
      if password1 != password2:
        return '两次密码不一致'
      else:
        user = User(telephone = telephone,username=username,password=password1,img_url = img_url)
        db.session.add(user)
        ###排查排查插入问题 注册插入数据报错(id must Intgeter)
        db.session.commit()
        return redirect(url_for('login'))

@app.route('/login/',methods=['GET','POST'])
#登陆路由
def login():
  # remove the username from the session if it's there
    if request.method == 'GET':
      return render_template('login.html')
    else:
      telephone = request.form['telephone']
      password = request.form['password']
      #判断用户名密码是否一致
      user = User.query.filter(User.telephone == telephone,User.password == password).first()
      if user:
        #存放session的用户id
        session['user_id'] = user.id
        session.permanet = True
        ###设置seeson过期
        app.permanent_session_lifetime = timedelta(minutes=30)
        return redirect(url_for('index'))
      else:
        return '用户名密码错误'

@app.route('/logout/')
#注销路由
def logout():
  # session.clear()
  session.pop('user_id')
  return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
# 判断用户是否登陆，否则返回登陆页面的路由装饰器
@login_req
#问题文章路由
def question():
  # remove the username from the session if it's there
  if request.method == 'GET':
    return render_template('question.html')
  else:
    title  = request.form['title']
    context = request.form['context']
    user_id = session.get('user_id')
    username = (User.query.filter(User.id == user_id ).first()).username
    questions = Question(title=title,context=context,author_id= user_id,username=username)
    db.session.add(questions)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/detail/<question_id>')
#文章详情路由
def detail(question_id):
  # print(question_id)
  questions_model = Question.query.filter(Question.id == question_id ).first()
  # print(question_id)
  return render_template('detail.html',question=questions_model)



@app.route('/center/')
@app.route('/center/<int:page>/',methods=['GET', 'POST'])

#用户中心路由。
def center(page=None):
  page = int(request.args.get('page', 1))
  # 获取get请求传过来的以多少条数据分页的参数，默认为5
  per_page = int(request.args.get('per_page', 5))
  user_id = session.get('user_id')
  userpage = Question.query.filter(Question.author_id == user_id ).paginate(page, per_page, error_out=False)
  usertext = {
    'questions': userpage.items
  }
  # user_model = Question.query.filter(Question.author_id == user_id ).first()
  # print(question_id)
  return render_template('center.html',userpage=userpage,**usertext)

@app.route('/delete/<delete_id>',methods=['GET', 'POST'])
# 判断用户是否登陆，否则返回登陆页面的路由装饰器
@login_req
#删除用户文章的路由
def delete(delete_id):
  if request.method == 'GET':
    return render_template('index.html')
  else:
    #判断用户id是否一致，才去删除
    user_id = session.get('user_id')
    userid = Question.query.filter(Question.author_id == user_id).first()
    if userid :
      dele = Question.query.filter(Question.id == delete_id).first()
      db.session.delete(dele)
      db.session.commit()
      return redirect(url_for('index'))
    else:
      return  '没有权限删除'



@app.route('/upload', methods=['POST', 'GET'])
def upload():
  if request.method == 'POST':
    f = request.files['file']
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    print(f.filename)
    uploadfile = basepath + '/static/images'
    upload_path = os.path.join( uploadfile,secure_filename(f.filename))
    f.save(upload_path)
    user_id = session.get('user_id')
    userimg = User.query.filter(User.id == user_id ).first()
    userimg.img_url = f.filename
    db.session.commit()
    return redirect(url_for('center'))
  return render_template('center.html')


###HOOK 函数
@app.context_processor
##装修{% if user %}
def my_context_processoer():
  user_id = session.get('user_id')
  if user_id:
    user = User.query.filter(User.id == user_id).first()
    if user:
      return {'user':user}
  return {}
###HOOK 函数
# 删除功能hook
@app.context_processor
def my_context_delete():
  user_id = session.get('user_id')
  if user_id:
    dele1 = Question.query.filter_by(author_id = user_id).first()
    user = User.query.filter_by(id = user_id).first()
    # print(user.username)
    # print(dele1.username)
    if dele1:
        return {'dele1':dele1}
    #### 无论如何都要返回空
  return {}
##监听端口
app.run(host='0.0.0.0')

# @app.route('/hidw/<a>',methods=['GET', 'POST']))
# def hid():
#     return (index)
# # if request.method == 'GET':
# #     return render_template('index.html')
# # else:
# #
# #     ##update
# #     a = Question.query.filter(Question.id == a).first()
# #     a.hid='hidden'
# #     db.session.commit()
# #     return redirect(url_for('index'))