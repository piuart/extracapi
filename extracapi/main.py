from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


#-------------------------------------------------------------------


from fastapi import Depends, HTTPException, status
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi import Depends, HTTPException, Header
from starlette.responses import RedirectResponse


#-------------------------------------------------------------------

import os
from slave_url import slaveUrl
from slave_file import slaveFile
from login import user as userModel


#-------------------------------------------------------------------


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



#-------------------------------------------------------------------





SECRET = "secret-key"
manager = LoginManager(SECRET, token_url="/logmein",use_cookie=True)
manager.cookie_name = "some-name"


@manager.user_loader
def user_loader(userName):
    user = userModel.getUser(userName)
    return user
    



#------------------------------------------------------------------



@app.get("/")
def index( request: Request):
    return templates.TemplateResponse("index.html", { 'request': request })



@app.get("/login")
def login( request: Request):
    return templates.TemplateResponse("login/login.html", { 'request': request }) 



#--------------------------------------------------------------------------------


@app.post("/logmein")
async def logmein(form: OAuth2PasswordRequestForm = Depends()):
    userName = form.username
    password = form.password
    user = user_loader(userName)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    elif password != user["password"]:
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token = manager.create_access_token(
        data={"sub":user['username']}
    )
    resp = RedirectResponse(url="/dashboard",status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp,access_token)
    print(access_token)
    return resp

@app.get("/login_user", response_class=HTMLResponse)
async def login_user(request: Request, username: str, token:str =Depends(manager)):
    print('entraste aqui ')
    return templates.TemplateResponse("dashboard/dashboard.html", {"request": request, "username": username})

@app.get("/register", response_class=HTMLResponse)
async def register(request : Request):
    return templates.TemplateResponse("login/register.html", {"request" : request})



@app.post("/register/authen")
async def register(form : OAuth2PasswordRequestForm = Depends()):
    userName = form.username
    password = form.password
    if userModel.checkUserName(userName):
        userModel.addUser(userName, password)
    else:
        raise HTTPException(status_code=400, detail="El Usuario ya existe")
    return RedirectResponse(url="/",status_code=status.HTTP_302_FOUND)



#-------------------------------------------------------------------




@app.get('/logout', response_class=HTMLResponse)
def logout(request: Request, user=Depends(manager)):
    resp = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, "")
    return resp  


#----------------ANÁLISIS DE URL-------------------------------------


@app.get('/dashboard/')
def dashboard(request : Request, user=Depends(manager)):
    return templates.TemplateResponse("dashboard/dashboard.html", context={"request": request, "username": user["username"]}) 



@app.post('/dashboard/')
def dashboard(request : Request, user=Depends(manager), ulr : str = Form(...)):
    ur = ulr
    print(ur)
    js = slaveUrl(ur)
    return templates.TemplateResponse("dashboard/dashboard.html", context={"request": request, "username": user["username"] , "urls": js, "resultado": " "}) 


#---------------ANÁLISIS DE ARCHIVOS O FICHEROS--------------------------------------


@app.get('/test_file/')
def test_file(request : Request, user=Depends(manager)):
    return templates.TemplateResponse("dashboard/test_file.html", {"request": request, "username": user["username"]})


@app.post('/test_file/')
def test_file(request : Request, user=Depends(manager), archive : str = Form(...)):
    file = archive
    simple_path = './files/'
    route_simp_path = simple_path.replace("/","/")
    print('----------------------------------------')
    print(route_simp_path)
    abs_path = os.path.abspath(simple_path+file)
    new_route = os.path.join(abs_path)
    print(new_route)
    js = slaveFile(new_route)
    return templates.TemplateResponse("dashboard/test_file.html", context={"request": request,"username": user["username"], "urls": file, "urls_path": js, "resultado": " " }) 
