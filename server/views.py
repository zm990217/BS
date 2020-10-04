import datetime
import json
import traceback

import jwt
from jwt import exceptions
from flask import Blueprint, request, jsonify, make_response, session
from app import db
from app.models import User, Question, Wj, Answer, Submit, Options

views = Blueprint('views', __name__)

def create_token(id, name):
    SALT = 'zm'
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload = {
        'user_id': id,
        'username': name,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers).decode('utf-8')
    return token

def get_payload(token):
    SALT = 'zm'
    try:
        jwt.decode(token, SALT, True)
        return True
    except:
        return False

@views.route('/api/design',methods=['POST'])
def designOpera():
    params = request.json
    res={'code':0,'msg':'success'}
    print(params)
    if params['opera_type'] == 'login':
        res = login(params)
    elif params['opera_type'] == 'register':
        res = register(params)
    elif params['opera_type'] == 'resetPasswd':
        res = resetPasswd(params)
    elif params['opera_type'] == 'add_wj':
        res = addWj(params)
    elif params['opera_type'] == 'get_wj_list':
        res = getWjList(params)
    elif params['opera_type'] == 'delete_wj':
        res = deleteWj(params)
    elif params['opera_type'] == 'add_question':
        res = addQuestion(params)
    elif params['opera_type'] == 'get_question_list':
        res = getQuestionList(params)
    elif params['opera_type'] == 'delete_question':
        res = deleteQuestion(params)
    elif params['opera_type'] == 'push_wj':
        res = pushWj(params)
    elif params['opera_type'] == 'get_options_list':
        res = getOptionsList(params)
    elif params['opera_type'] == 'get_answer_list':
        res = getAnswerList(params)
    return jsonify(res)

def login(params):   
    username = params['username']
    password = params['password']

    user = User.query.filter_by(username = username).first()
    if user == None:
        res = {
            'code': 500,
            'msg': '用户不存在'
        }
        return res   
    if user.check_password(password):
        token = create_token(user.username, user.password)
        res = {
            'username': user.username,
            'token': token,
            'code': 0,
            'msg': '登录成功'
        }
    else:
        res = {
            'code': 501,
            'msg': '账号或密码错误'
        }
    return res

def register(params):
    username = params['username']
    password = params['password']
    email = params['email']

    user1 = User.query.filter_by(username = username).first()
    if user1 is not None:
        res = {
            'code': 500,
            'msg': '该账号已存在'
        }
        return res
    user2 = User.query.filter_by(email = email).first()
    if user2 is not None:
        res = {
            'code': 501,
            'msg': '该邮箱已存在'
        }
        return res
    user = User(username = username, password=password, email=email)
    db.session.add(user)
    db.session.commit()

    res = {
        'code': 0,
        'msg': '注册成功'
    }
    return res

def resetPasswd(params):
    res = {'code': 0, 'msg': 'success'}
    username = params['username']
    oldpassword = params['oldpassword']
    newpassword = params['newpassword']
    user = User.query.filter_by(username = username).first()
    if user == None:
        res = {
            'code': 500,
            'msg': '该账号不存在'
        }
        return res
    else:
        if user.check_password(oldpassword):
            user.password = newpassword
            db.session.commit()
        else :
            res = {
                'code': -1,
                'msg': '密码错误'
            }
    return res

def addWj(params):
    res = {'code': 0, 'msg': 'success'}
    username = params['username']
    title = params['title']
    desc = params['desc']
    id = params['id']
    permissions = params['permissions']
    endTime = params['endTime']
    if username and title:
        try:
            if id:
                wj = Wj.query.filter_by(username = username, id = id).first()
                wj.title = title
                wj.desc = desc
                wj.permissions = permissions
                wj.endTime = endTime
                db.session.commit()
            else :
                wj = Wj(username=username, title=title,desc=desc, status=0, endTime=endTime, permissions=permissions)
                db.session.add(wj)
                db.session.commit()
        except:
            res['code'] = '-4'
            res['msg'] = '操作失败'
        else:
            if wj.id > 0 :
                res['id'] = wj.id
            else:
                res['code'] = '-4'
                res['msg'] = '操作失败'
    else:
        res['code'] = '-3'
        res['msg'] = '确少必要参数'
    return res

def getWjList(params):
    res = {'code': 0, 'msg': 'success'}
    username = params['username']
    if username:
        obj = Wj.query.filter_by(username=username).order_by(Wj.id.desc()).all()
        detail = []
        for item in obj:
            temp = {}
            temp['id']=item.id
            temp['title']=item.title
            temp['desc']=item.desc
            if item.status == 0:
                temp['status']="未发布"
            else:
                temp['status']="已发布"
            if item.permissions == 'allPrem':
                temp['permissions'] = '不限制'
            elif item.permissions == 'onlyUser':
                temp['permissions'] = '仅限注册用户'
            elif item.permissions == 'timeUser':
                temp['permissions'] = '仅限注册用户且最多填写3次'
            elif item.permissions == 'timeAll':
                temp['permissions'] = '不限制用户但最多3次' 
            else:
                temp['permissions'] = '不限制'  
            temp['endTime'] = item.endTime
            detail.append(temp)
        res['data'] = {'detail':detail}
    else:
        res['code'] = '-3'
        res['msg'] = '确少必要参数'
    return res

def deleteWj(params):
    res = {'code': 0, 'msg': 'success'}
    username = params['username']
    wjId = params['wjId']
    wj = Wj.query.filter_by(id=wjId).first()
    if username == wj.username:
        try:
            answers = Answer.query.filter_by(wjId = wjId).all()
            for answer in answers:
                db.session.delete(answer)
                db.session.commit()
            submits = Submit.query.filter_by(wjId = wjId).all()
            for submit in submits:
                db.session.delete(submit)
                db.session.commit()
            questions = Question.query.filter_by(wjId = wjId).all()
            for question in questions:
                options = Options.query.filter_by(questionId = question.id).all()
                for option in options:
                    db.session.delete(option)
                    db.session.commit()
                db.session.delete(question)
                db.session.commit()
            db.session.delete(wj)
            db.session.commit()
        except:
            res['code'] = '-4'
            res['msg'] = '操作失败'
    else:
        res['code'] = '-3'
        res['msg'] = '权限错误'
    return res

def addQuestion(params):
    res = {'code': 0, 'msg': 'success'}
    username = params['username']
    wjId = params['wjId']
    questionTitle = params['title']
    questionType = params['type']
    options = params['options']
    row = params['row']
    must = params['must']
    casc = params['casc']
    questionId = params['questionId']
    if (wjId and questionTitle and questionType and must and username) != None:
        if questionType in ['radio','checkbox','text','score','number']:
            if questionId:
                ques =  Question.query.filter_by(id=questionId,wjId=wjId).first()
                ques.title = questionTitle
                ques.type = questionType
                ques.row = row
                ques.must = must
                ques.casc = casc
                db.session.commit()
                newOptionsID = []
                for temp in options:
                    newOptionsID.append(temp['id'])
                oldOptions = Options.query.filter_by(questionId=questionId).all()
                for option in oldOptions:
                    if option.id not in newOptionsID:
                        db.session.delete(option)
                        db.session.commit()
                for option in options:
                    if option['id'] != 0:
                        opt = Options.query.filter_by(id = option['id']).first()
                        opt.title = option['title']
                        db.session.commit()
                    else:
                        opt = Options(questionId=questionId,title=option['title'])
                        db.session.add(opt)
                        db.session.commit()
            else:
                obj = Question(wjId=wjId,title=questionTitle,type=questionType,row=row,must=must,casc=casc)
                db.session.add(obj)
                db.session.commit()
                questionId = obj.id
                res['id'] = obj.id
                if questionType in ['radio','checkbox','score']:
                    if options and type(options) == type([]):
                        for item in options:
                            opt = Options(questionId=questionId, title=item['title']) 
                            db.session.add(opt)
                            db.session.commit()
                    else:
                        res['code'] = '-4'
                        res['msg'] = '操作失败'
        else:
            res['code'] = '-5'
            res['msg'] = '传入参数值有误'
    else:
        res['code'] = '-3'
        res['msg'] = '缺少参数'
    return res           

def getQuestionList(params):
    res = {'code': 0, 'msg': 'success'}
    wjId = params['wjId']
    username = params['username']
    if username:
        wj = Wj.query.filter_by(id = wjId).first()
        if wj.username == username:
            obj = Question.query.filter_by(wjId = wjId).all()
            detail = []
            for item in obj:
                temp = {}
                temp['title'] = item.title
                temp['type'] = item.type
                temp['id'] = item.id
                temp['row'] = item.row
                temp['must'] = item.must
                if item.casc != '' and item.casc != None:
                    casc = eval(item.casc)
                    qId = casc[0]
                    optId = casc[1]
                    qTitle = Question.query.filter_by(id = qId).first()
                    temp['cascQuestion'] = qTitle.title
                    optTitle = Options.query.filter_by(id = optId).first()
                    temp['cascOption'] = optTitle.title
                    temp['casc'] = item.casc
                else:
                    temp['cascQuestion'] = ''
                    temp['cascOption'] = ''
                    temp['casc'] = ''
                temp['options'] = []
                if temp['type'] in ['radio', 'checkbox', 'score']:
                    opt = Options.query.filter_by(questionId = item.id).all()
                    for optItem in opt:
                        temp['options'].append({'title': optItem.title, 'id': optItem.id})
                temp['radioValue'] = -1
                temp['checkboxValue'] = []
                temp['textValue'] = ''
                temp['numberValue'] = ''
                temp['scoreValue'] = -1
                detail.append(temp)
            res['detail'] = detail
        else:
            res['code'] = '-6'
            res['msg'] = '权限不足'
    else:
        res['code'] = '-3'
        res['msg'] = '缺少参数'
    return res

def deleteQuestion(params):
    res = {'code': 0, 'msg': 'success'}
    questionId = params['questionId']
    if questionId:
        try:
            answers = Answer.query.filter_by(questionId=questionId).all()
            for answer in answers:
                db.session.delete(answer)
                db.session.commit()
            options = Options.query.filter_by(questionId=questionId).all()
            for opt in options:
                db.session.delete(opt)
                db.session.commit()
            ques = Question.query.filter_by(id = questionId).first()
            db.session.delete(ques)
            db.session.commit()
        except:
            res['code'] = '-4'
            res['msg'] = '操作失败'
    else:
        res['code'] = '-3'
        res['msg'] = '缺少参数'
    return res

def pushWj(params):
    res = {'code': 0, 'msg': 'success'}
    status = params['status']
    wjId = params['wjId']
    if wjId:
        try:
            wj = Wj.query.filter_by(id = wjId).first()
            wj.status = status
            db.session.commit()
            res['status'] = status
        except:
            res['code'] = '-4'
            res['msg'] = '操作失败'
    else:
        res['code'] = '-3'
        res['msg'] = '缺少参数'
    return res

def getOptionsList(params):
    res = {'code': 0, 'msg': 'success'}
    wjId = params['wjId']
    questionId = params['questionId']
    username = params['username']
    if username:
        try:
            obj = Question.query.filter_by(wjId = wjId).all()
            detail = []
            if questionId == 0:
                for item in obj:
                    if item.type == 'radio':
                        temp = {}
                        temp['value']=item.id
                        temp['label']=item.title
                        temp['children']=getOptions(item.id)
                        detail.append(temp)
            else :
                for item in obj:
                    if item.type == 'radio' and item.id < questionId:
                        temp = {}
                        temp['value']=item.id
                        temp['label']=item.title
                        temp['children']=getOptions(item.id)
                        detail.append(temp)
            res['detail'] = detail
        except:
            res['code'] = '-4'
            res['msg'] = '操作失败'
    else:
        res['code'] = '-3'
        res['msg'] = '缺少参数'
    return res

def getOptions(questionId):
    options = Options.query.filter_by(questionId=questionId).all()
    sub = []
    for option in options:
        result={}
        result['value']=option.id
        result['label']=option.title
        sub.append(result)
    return sub

def getAnswerList(params):
    res={'code':0,'msg':'success'}
    wjId = params['wjId']
    if wjId:
        #try:
            obj = Question.query.filter_by(wjId=wjId).all()
            res['detail']=[]
            for question in obj:
                if question.type in ['radio','checkbox','score']:
                    item = {}
                    item['title'] = question.title
                    item['type'] = question.type
                    item['countShow']=[]
                    options = Options.query.filter_by(questionId=question.id).all()
                    allAns = Answer.query.filter_by(questionId=question.id).all()
                    allCount = len(allAns)
                    for option in options:
                        countShow={}
                        countShow['optionTitle'] = option.title
                        subAns = Answer.query.filter_by(questionId=question.id,answer=option.id).all()
                        count = len(subAns)
                        countShow['count'] = count
                        if allCount == 0:
                            countShow['per'] = '0%'
                        else:
                            countShow['per'] = str(round(count/allCount*100,2))+'%'
                        item['countShow'].append(countShow)
                    res['detail'].append(item)
                elif question.type == 'text':
                    item = {}
                    item['title'] = question.title
                    item['type'] = question.type
                    item['answer'] = []
                    answers = Answer.query.filter_by(questionId=question.id).all()
                    for answer in answers:
                        content={}
                        if answer.answer!='':
                            content['content']=answer.answer
                            item['answer'].append(content)
                    res['detail'].append(item)
                elif question.type == 'number':
                    item = {}
                    item['title'] = question.title
                    item['type'] = question.type
                    item['answer'] = []
                    answers = Answer.query.filter_by(questionId=question.id).all()
                    s=0
                    c=0
                    for answer in answers:
                        content={}
                        if answer.answer!='':
                            content['flag'] = ''
                            content['number'] = answer.answer
                            c+=1;s+=int(answer.answer)
                            item['answer'].append(content)
                    content={}
                    content['flag']='平均数'
                    if c!=0:
                        content['number'] = str(round(s/c,2))
                    else:
                        content['number'] = '0'
                    item['answer'].append(content)
                    res['detail'].append(item)
        #except:
        #   res['code'] = '-4'
        #   res['msg'] = '操作失败'
    else:
        res['code'] = '-3'
        res['msg'] = '缺少参数'
    return res

@views.route('/api/answer',methods=['POST'])
def answerOpera():
    params = request.json
    ip = request.remote_addr
    res={'code':0,'msg':'success'}
    print(params)
    if params['opera_type'] == 'get_info':
        res = getInfo(params)
    elif params['opera_type'] == 'submit_wj':
        res = submitWj(params,ip)
    return jsonify(res)

def getInfo(params):
    res={'code':0,'msg':'success'}
    wjId = params['wjId']
    username = params['username']
    if wjId:
        try:
            wj = Wj.query.filter_by(id = wjId).first()
            res['title'] = wj.title
            res['desc'] = wj.desc
            res['permissions']=wj.permissions
            if wj.permissions == 'timeUser' or wj.permissions == 'timeAll':
                numObj=Submit.query.filter_by(wjId=wjId).all()
                tempn = {}
                tempn['number']=None
                for item in numObj:
                    if item.number != None:
                        tempn['number'] = int(item.number)
                if tempn['number']==None:
                    res['number']=3
                else:
                    res['number']=tempn['number']
            else:
                res['number'] = -1
            if wj.status==1 or username==wj.username:
                obj = Question.query.filter_by(wjId=wjId).all()
                detail = []
                for item in obj:
                    temp = {}
                    temp['title'] = item.title
                    temp['type'] = item.type
                    temp['id'] = item.id 
                    temp['row'] = item.row
                    temp['must'] = item.must
                    temp['options'] = []
                    if temp['type'] in ['radio', 'checkbox','score']:
                        optionItems = Options.query.filter_by(questionId=item.id).all()
                        for optionItem in optionItems:
                            temp['options'].append({'title':optionItem.title,'id':optionItem.id})
                    temp['radioValue'] = -1 
                    temp['checkboxValue'] = []
                    temp['textValue'] = '' 
                    temp['numberValue'] = ''
                    temp['score'] = -1 
                    if item.casc != None and item.casc!='':
                        casc=eval(item.casc)
                        qId=casc[0]
                        optId=casc[1]
                        temp['casc_questionId']=qId
                        temp['casc_optionId']=optId
                        temp['casc']=item.casc
                    else:
                        temp['casc_questionId']=-1
                        temp['casc_optionId']=-1
                        temp['casc']=''
                    detail.append(temp)
                res['detail'] = detail
            else:
                res['code'] = '-10'
                res['msg'] = '问卷尚未发布'
        except:
            res['code'] = '-4'
            res['msg'] = '操作失败'
    else:
        res['code'] = '-3'
        res['msg'] = '缺少参数'
    return res

def submitWj(params,ip):
    res={'code':0,'msg':'success'}
    wjId = params['wjId']
    useTime = params['useTime']
    detail = params['detail']
    number = params['number']
    for item in detail:
        if item['type'] == 'radio' and item['must'] == 1 and item['radioValue'] == -1:
            res['code'] = '-4'
            res['msg'] = '必答题未答'
            return res
        elif item['type'] == 'checkbox' and item['must'] == 1 and len(item['checkboxValue']) == 0:
            res['code'] = '-4'
            res['msg'] = '必答题未答'
            return res
        elif item['type'] == 'text' and item['must'] == 1 and item['textValue'] == '':
            res['code'] = '-4'
            res['msg'] = '必答题未答'
            return res
        elif item['type'] == 'number' and item['must'] == 1 and item['numberValue'] == '':
            res['code'] = '-4'
            res['msg'] = '必答题未答'
            return res
        elif item['type'] == 'score' and item['must'] == 1 and item['scoreValue'] == -1:
            res['code'] = '-4'
            res['msg'] = '必答题未答'
            return res
    wj = Wj.query.filter_by(id=wjId).first()
    if wj.status == 0:
        res['code'] = '-10'
        res['msg'] = '问卷尚未发布'
        return res
    if number == -1:
        submit = Submit(wjId=wjId,submitTime=datetime.datetime.now(),submitIp=ip,useTime=useTime,number=number)
    else:
        submit = Submit(wjId=wjId,submitTime=datetime.datetime.now(),submitIp=ip,useTime=useTime,number=number-1)
    db.session.add(submit)
    db.session.commit()

    for item in detail:
        if item['type'] != 'checkbox':
            index=item['type']+'Value'
            answer = Answer(questionId=item['id'],submitId=submit.id,wjId=wjId,type=item['type'],answer=item[index])
            db.session.add(answer)
            db.session.commit()
        else:
            for value in item['checkboxValue']:
                answer = Answer(questionId=item['id'],submitId=submit.id,wjId=wjId,type=item['type'],answer=value)
                db.session.add(answer)
                db.session.commit()
    return res