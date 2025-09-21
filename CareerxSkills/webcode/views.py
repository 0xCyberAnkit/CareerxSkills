from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import mysql.connector as mydb
# Create your views here.
def server():
    global con,cur
    con = mydb.connect(host="careerxskills.mysql.pythonanywhere-services.com",user="careerxskills",password="Ankit1234",database="careerxskills$default")
    cur = con.cursor()
def index(request):
    data = {'path':'auth'}
    email = request.session.get('email')
    if email:
        data['path'] = 'dashboard'
    return render(request,"index.html",data)
def dashboard(request):
    email = request.session.get('email')
    if not email:
        return redirect("/")
    server()
    cur.execute(f"select * from users join profile on users.id = profile.id where email = '{email}' ;" )
    profile = cur.fetchall()
    data = {
        'logo' : profile[0][4][0],
        'name' : profile[0][4]
        }
    return render(request,"dashboard.html",data)
def auth(request):
    request.session['email'] = None
    server()
    if request.method == 'POST':
        data = {}
        if request.POST.get('mode') == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            cur.execute("select * from users where email = %s and password = %s ;" ,(email,password))
            profile = cur.fetchall()
            if profile:
                request.session['email'] = profile[0][1]
                data['verified'] = 'verified'
            else:
                data['a'] = 'a'
            return JsonResponse(data)
        else:
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            repeatpass = request.POST.get('repass')
            cur.execute(f"select * from users where email = '{email}';")
            if cur.fetchall():
                data['error'] = 'accounterror'
            elif password != repeatpass:
                data['error'] = 'passworderror'
            else:
                data['success'] = 'success'
                cur.execute("insert into users (email,password) values (%s,%s);",(email,password))
                con.commit()
                cur.execute("insert into profile values (%s,%s,%s,%s,%s,%s) ;" ,(cur.lastrowid,name,"",'{}','{}','{}'))
                con.commit()
            return JsonResponse(data)
    return render(request,'auth.html')
def aiadvisor(request):
    email = request.session.get('email')
    if not email:
        return redirect('/')
    return render(request,'ai.html')
def roadmap(request):
    email = request.session.get('email')
    if not email:
        return redirect('/')
    return render(request,'roadmap.html')
def profile(request):
    email = request.session.get('email')
    if not email:
        return redirect('/')
    server()
    cur.execute(f"select * from users join profile on users.id = profile.id where email = '{email}' ;" )
    profile = cur.fetchall()
    data = {
        'logo' : profile[0][4][0].upper(),
        'name' : profile[0][4],
        'email' : profile[0][1]
        }
    return render(request,'profile.html',data)
def dev(request):
    return render(request,'dev.html')