#coding=utf-8
from flask import Flask,url_for
from flask import make_response
from flask import request
from flask import render_template
import sys 
import string
import re
import requests
app = Flask(__name__)


def pelogin(user,pwd):
    url='http://202.120.127.149:8989/spims/login.do?method=toLogin'
    postData={'UNumber':user,'Upwd':pwd,'USnumber':u'上海大学'}
    s = requests.Session()
    try:
        r = s.get('http://202.120.127.149:8989/spims/login/index.jsp',timeout=10)
        r = s.post(url,data=postData,timeout=10)
        r = s.get('http://202.120.127.149:8989/spims/exercise.do?method=seacheload',timeout=10)
    except:
        return False
    else:
        table_p=r'<table cellpadding="3" cellspacing="1" class="table_bg">([\s\S]*)<tr>\s+<td colspan="13">'
        content=re.findall(table_p, r.text,re.S|re.M)
        if(len(content)==0):
            return False
        return content[0]

def finoldlogin(user,pwd):
    url='http://finance.shu.edu.cn/Login.aspx?ReturnUrl=%2fTuition.aspx'
    postData={'__EVENTTARGET':'',
    '__EVENTARGUMENT':'',
    '__VIEWSTATE':'/wEPDwUKLTM3NDg5MjY1NQ9kFgICAQ9kFgICAw9kFhACAQ8PFgIeBFRleHQFNw0KCQkJCQkJCQkJCTxiPueZu+W9leezu+e7nzwvYj7vvIjmnKznp5HmlLbotLnmn6Xor6LvvIlkZAIDDw8WAh4LTmF2aWdhdGVVcmwFNExvZ2luLmFzcHg/UmV0dXJuVXJsPSUyZlR1aXRpb24uYXNweCZFbXBsb3llZUxvZ2luPTFkZAITDw8WAh4HVmlzaWJsZWdkZAIUDw8WBB8ABcQBPGltZyBzcmM9cGljLzEuZ2lmIGJvcmRlcj0wPjxpbWcgc3JjPXBpYy8xLmdpZiBib3JkZXI9MD48aW1nIHNyYz1waWMvNS5naWYgYm9yZGVyPTA+PGltZyBzcmM9cGljLzUuZ2lmIGJvcmRlcj0wPjxpbWcgc3JjPXBpYy84LmdpZiBib3JkZXI9MD48aW1nIHNyYz1waWMvNy5naWYgYm9yZGVyPTA+PGltZyBzcmM9cGljLzQuZ2lmIGJvcmRlcj0wPh8CZ2RkAhYPDxYCHwJnZGQCFw8PFgQfAAWoATxpbWcgc3JjPXBpYy81LmdpZiBib3JkZXI9MD48aW1nIHNyYz1waWMvNS5naWYgYm9yZGVyPTA+PGltZyBzcmM9cGljLzUuZ2lmIGJvcmRlcj0wPjxpbWcgc3JjPXBpYy83LmdpZiBib3JkZXI9MD48aW1nIHNyYz1waWMvMi5naWYgYm9yZGVyPTA+PGltZyBzcmM9cGljLzQuZ2lmIGJvcmRlcj0wPh8CZ2RkAhkPDxYCHwJnZGQCGw8PFgIfAmdkZGTkUiQcxLjI7qbIyEZc3bENY5Ztjw==',
    '__EVENTVALIDATION':'/wEWBAKXm79JAtXh0pgPAqW0mtsGApOzq+INgXLh/Sj8FgD/gUxZsNSw4Q5MHNc=',
    'login1$txtName':user,
    'login1$txtPsw':pwd,
    'login1$Button1':''}
    s = requests.Session()
    r = s.post(url,data=postData,timeout=30)
    string = re.search(r'<table id="Table1" cellspacing="0" cellpadding="0" width="759" align="center" border="0">([\s\S]*)</table>',r.text,flags=0).group(0)
    string = re.sub(r'<span id="Tuition1_Label2">([\s\S]*)</select>', "", string)
    string = re.sub(r"<font color='red'>([\s\S]*?)</font>", "", string)
    return string


def lehulogin(user,pwd):
    postData={'username':user,'password':pwd,'url':'http://www.lehu.shu.edu.cn/'}
    s = requests.Session()
    try:
        r = s.post('http://passport.lehu.shu.edu.cn/ShowOrgUserInfo.aspx',data=postData,timeout=30)
        r = s.get('http://card.lehu.shu.edu.cn/CardTradeDetail.aspx',timeout=30)
    except:
        return False
    else:
        table_p = r'<span id="ctl00_Contentplaceholder1_Label1">([\s\S]*)</form>'
        content = re.findall(table_p,r.text,re.S|re.M)
        if(len(content)==0):
            return False
        else:
            return content[0]
    return False

@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    return resp

@app.route('/cal')
def cal():
    resp = make_response(render_template('cal.html'))
    return resp

def finquest():
    from PIL import Image
    from io import BytesIO
    s = requests.Session()
    r = s.get('http://xssf.shu.edu.cn:8100/SFP_Share/Home/CheckImgCode',timeout=10)
    return BytesIO(r.content).getvalue().encode('base64') , s.cookies

def finlogin(cookies,user,pwd,check):
    postData={'userName':user,
    'pwd':pwd,
    'ktextbox':check,
    'hidCheckCode':''}
    s = requests.Session()
    try:
        r = s.post('http://xssf.shu.edu.cn:8100/SFP_Share/?Length=5',data=postData,timeout=10,cookies=cookies)
        r = s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_PersonInfo',timeout=10)
        personinfo = re.search(r'(<fieldset([\s\S]*)</fieldset>)',r.text,flags=0).group(0)
        r =s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryPaymentcondition',timeout=10)
        paymentcondition = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
        arrearageAmount = re.search(r'[0-9]\d*.[0-9]\d*',r.text,flags=0).group(0)
        personinfo = re.sub(r'<span id="arrearageAmount"></span>',arrearageAmount,personinfo)
        r = s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryChargeRecord',timeout=10)
        chargerecord = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
        r = s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryRefundRecord',timeout=10)
        refundrecord = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
        string = personinfo+u'<legend></legend><legend>缴费情况</legend>'+paymentcondition+u'<legend>缴费记录</legend>'+chargerecord+u'<legend>退费记录</legend>'+refundrecord+u'<legend></legend>'
        string = re.sub(r'<table class="tblList tblInLine">','<table class="table table-hover">',string)
    except:
        return False
    else:
        return string

def phyquest():
    from PIL import Image
    from io import BytesIO
    s = requests.Session()
    r = s.get('http://www.phylab.shu.edu.cn/openexp/index.php/Public/login/',timeout=10)
    phyhash = re.search(r'<input type="hidden" name="__hash__" value="([\s\S]*)" />',r.text,flags=0).group(1)
    r = s.get('http://www.phylab.shu.edu.cn/openexp/index.php/Public/verify/',timeout=10)
    return BytesIO(r.content).getvalue().encode('base64') , s.cookies ,phyhash

def phylogin(cookies,hash,user,pwd,check):
    postData={'_hash_':hash,
    'account':user,
    'ajax':'1',
    'password':pwd,
    'verify':check}
    s = requests.Session()
    try:
        r = s.post('http://www.phylab.shu.edu.cn/openexp/index.php/Public/checkLogin/',data=postData,timeout=10,cookies=cookies)
        r = s.get('http://www.phylab.shu.edu.cn/openexp/index.php/Public/main',timeout=10,cookies=cookies)
        string = re.search(r'(<TABLE([\s\S]*?)</TABLE>)',r.text,flags=0).group(0)
        string = re.sub(r'<TABLE id="checkList" class="list" cellpadding=0 cellspacing=0 >','<table class="table table-hover" cellpadding="0" cellspacing="0" >',string)
        string = re.sub(r'<input type="submit" name="submit1"','<input type="submit" name="submit1" class="btn btn-large btn-info" ',string)
    except:
        return False
    else:
        return string

 
@app.route('/phy',methods=['POST', 'GET'])
def phy():
    error = None
    if request.method == 'POST':
        usercookies = requests.cookies.RequestsCookieJar()
        usercookies.set('PHPSESSID',request.cookies.get('PHPSESSID'))
        r = phylogin(usercookies,request.cookies.get('_hash_'),request.form['username'],request.form['password'],request.form['check'])
        if r != False:
            resp = make_response(render_template('phy.html', r=r))
            return resp
        else:
            error = u'登录失败！可能是账户密码错误或服务器宕机'
            return render_template('index.html', error=error)
    elif request.method == 'GET':
        r,cookies,phyhash = phyquest()
        error = u'请注意！若未修改过密码，初始密码为学号！！'
        resp = make_response(render_template('loginp.html',r=r,error=error))
        for cj in cookies:
            resp.set_cookie(cj.name,cj.value)
        resp.set_cookie('_hash_',phyhash)
        return resp
        
    return render_template('index.html', error=error)
@app.route('/fin',methods=['POST', 'GET'])
def fin():
    error = None
    if request.method == 'POST':
        usercookies = requests.cookies.RequestsCookieJar()
        usercookies.set('ASP.NET_SessionId',request.cookies.get('ASP.NET_SessionId'),domain='shu.edu.cn')
        usercookies.set('SFP_Verify_Cookie',request.cookies.get('SFP_Verify_Cookie'),domain='shu.edu.cn')
        r = finlogin(usercookies,request.form['username'],request.form['password'],request.form['check'])
        if r != False:
            resp = make_response(render_template('fin.html', r=r))
            return resp
        else:
            error = u'登录失败！可能是账户密码错误或服务器宕机'
            return render_template('index.html', error=error)
    elif request.method == 'GET':
        r,cookies = finquest()
        resp = make_response(render_template('loginc.html',r=r))
        for cj in cookies:
            resp.set_cookie(cj.name,cj.value)
        return resp
    return render_template('index.html', error=error)

@app.route('/bus')
def bus():
    resp = make_response(render_template('bus.html'))
    return resp

@app.route('/map')
def map():
    resp = make_response(render_template('map.html'))
    return resp

@app.route('/login/<site>', methods=['POST', 'GET'])
def login(site):
    error = None
    if request.method == 'POST':
        if site == 'pe':
            r = pelogin(request.form['username'],request.form['password'])
        elif site == 'finold':
            r = finoldlogin(request.form['username'],request.form['password'])
        elif site == 'cardsurplus':
            r = lehulogin(request.form['username'],request.form['password'])
        else:
            r = False
        if r != False:
            return render_template(site+'.html', r=r)
        else:
            error = u'登录失败！可能是账户密码错误或服务器宕机'
            return render_template('index.html', error=error)
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

