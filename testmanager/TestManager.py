import sys
from flask import Flask, json, request,abort,g, render_template, redirect, url_for
from flask_jwt import JWT, jwt_required
from access_security import authenticate,identity
from testmanager.database import db_session, init_db
from testmanager.model.av_probe import Static_Probe
from testmanager.model.evaluation import Evidence
from testmanager.model.probem import Probem
from testmanager.model.user import User
from testmanager.tools.probeParser import ProbeParse
from testmanager.tools.probe_runner import runner_p
import subprocess

def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']


app = Flask(__name__)

app.config['SECRET_KEY'] = 'trentatre trentini'
jwt = JWT(app, authenticate, identity)





@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/login')
def log_in():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('signup.html')

@app.route('/api/token')
#@jwt_required()
def get_auth_token():
    token = g.user.generate_auth_token()
    #print "CIAO"
    return json.dumps({ 'token': token.decode('ascii') }), 201, {'Content-Type':'application/json'}


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/users',methods=['POST'])
@app.route('/signup',methods=['POST'])
def signup():
    print ("signup")
    print ("JSON received...")
    print request.json
    if request.json:
        username = request.json.get('username')
        password = request.json.get('password')
        print username
        print password
        if username is None or password is None:
            print "errore1"
            abort(400) # missing arguments
        u=User(username,password)
        db_session.add(u)
        #db_session.flush()
        try:
            db_session.commit()
        except:
            print "errore 2"
            e = sys.exc_info()[0]
            print e
            return json.dumps({'message':"errore "+e}), 500, {'ContentType':'application/json'}
        return json.dumps({'message':"user created"}), 201, {'ContentType':'application/json'}



@app.route('/probes/<probe_id>/evidence',methods=['GET'])
@jwt_required()
def list_evidences(probe_id):
    evs=Evidence.query.filter_by(id_probe=int(probe_id))
    result=[]
    for ev in evs:
        try:
            result.append({"time":str(ev.dtime),"result":str(bool(ev.result))})
        except:
            print "errore 2"
            e = sys.exc_info()
            print e
            print e
    return json.dumps(result),200


@app.route('/app')
def home():
    return render_template('home.html')

@app.route('/applications')
def apphome():
    return render_template('homeapp.html')

@app.route('/appvuln')
def vuln():
    return render_template('homevuln.html')

@app.route('/appenc')
def nmap():
    return render_template('homeenc.html')

@app.route('/appnet')
def net():
    return render_template('homenet.html')


@app.route('/resultenc',methods=['POST'])
def resultenc():
    port = request.form["port"]
    host=request.form["host"]
    message='<collector probe_driver="EncryptedChannelProbe" id="testsqlmap" cmid="testsqlmap"><TestCases><TestCase><ID>1</ID><TestInstance Operation="config"><Input>'
    message=message+'<Item key="port" value="'+port+'"/><Item key="host" value="'+host+'"/></Input></TestInstance></TestCase></TestCases></collector>'
    with open("/tmp/testEC.xml", "w") as text_file:
        text_file.write(message)
    #TODO: write xml for probe.py
    #proc=subprocess.Popen(, shell=True)
    #proc = subprocess.Popen(['python /root/probe.py', 'testEC.xml'],
    proc = subprocess.Popen(['cat', '/tmp/testEC.xml'],
                            shell=False,
                            stdout=subprocess.PIPE,
                            )
    stdout_value = proc.communicate()[0]
    print stdout_value
    return render_template('result.html',nameprobe="channel encryption",resultprobe=stdout_value)

@app.route('/resultvuln',methods=['POST'])
def resultvuln():
    category = request.form["category"]
    target=request.form["target"]
    CVSS=request.form["CVSS"]
    message='<collector probe_driver="probe_searchscan" id="probe_searchscan" cmid="probe_searchscan">   <TestCases>      <TestCase>         <ID>1</ID>         <TestInstance Operation="nessus">            <Input>               <Item key="host" value="https://localhost:8834" />               <Item key="login" value="admin" />               <Item key="password" value="password" />               <Item key="Insecure" value="True" />               <Item key="Target" value="'+target+'" />            </Input>         </TestInstance>         <TestInstance Operation="credentials">            <Input>               <Item key="PrivateKeyPath" value="" />               <Item key="certPass" value="" />               <Item key="certUser" value="" />               <Item key="ssh_user" value="" />               <Item key="ssh_pass" value="" />               <Item key="MySQL_user" value="" />               <Item key="MySQL_pass" value="" />               <Item key="MongoDB" value="" />               <Item key="MongoDB_user" value="" />               <Item key="MongoDB_pass" value="" />            </Input>         </TestInstance>         <TestInstance Operation="parameters">            <Input>               <Item key="Time" value="2012-12-31T00:00:00.000-00:00" />               <Item key="CVSS" value="'+CVSS+'" />               <Item key="Category" value="'+category+'" />            </Input>         </TestInstance>         <TestInstance Operation="mongo">            <Input>               <Item key="host" value="localhost" />               <Item key="port" value="27017" />            </Input>         </TestInstance>      </TestCase>   </TestCases></collector>'
    with open("/tmp/testEC.xml", "w") as text_file:
        text_file.write(message)
    #TODO: write xml for probe.py
    #proc=subprocess.Popen(, shell=True)
    #proc = subprocess.Popen(['python /root/probe.py', 'testEC.xml'],
    proc = subprocess.Popen(['cat', '/tmp/searchscan.xml'],
                            shell=False,
                            stdout=subprocess.PIPE,
                            )
    stdout_value = proc.communicate()[0]
    print stdout_value
    return render_template('result.html',nameprobe="channel encryption",resultprobe=stdout_value)

@app.route('/resultnet',methods=['POST'])
def resultnet():
    port = request.form["port"]
    host=request.form["host"]
    message='<collector probe_driver="EncryptedChannelProbe" id="testsqlmap" cmid="testsqlmap"><TestCases><TestCase><ID>1</ID><TestInstance Operation="config"><Input>'
    message=message+'<Item key="port" value="'+port+'"/><Item key="host" value="'+host+'"/></Input></TestInstance></TestCase></TestCases></collector>'
    with open("/tmp/testEC.xml", "w") as text_file:
        text_file.write(message)
    #TODO: write xml for probe.py
    #proc=subprocess.Popen(, shell=True)
    #proc = subprocess.Popen(['python /root/probe.py', 'testEC.xml'],
    proc = subprocess.Popen(['cat', '/tmp/testEC.xml'],
                            shell=False,
                            stdout=subprocess.PIPE,
                            )
    stdout_value = proc.communicate()[0]
    print stdout_value
    return render_template('result.html',nameprobe="channel encryption",resultprobe=stdout_value)



@app.route('/probes/<probe_id>/run',methods=['POST'])
@jwt_required()
def runProbe(probe_id):
    if request.method == 'POST':
        p=Probem.query.filter_by(id=probe_id).first()
        try:
            started=runner_p(p.id,p.doc)
        except:
            print "errore 2"
            e = sys.exc_info()
            print e
        #started=True
        if started:
            return json.dumps({"message":"probe id:"+str(probe_id)+" started correctly"}),200
        else:
            return json.dumps({"message":"error starting probe"+str(probe_id)+" check Test Agent logs"}),500

@app.route('/probes/<probe_id>',methods=['GET','DELETE'])
@jwt_required()
def manageProbe(probe_id):
    try:
        p=Probem.query.filter_by(id=int(probe_id)).first()
    except:
        print "errore 2"
        e = sys.exc_info()[0]
        print e
    if request.method == 'DELETE':
        #TODO: stop test if running
        db_session.remove(p)
        db_session.commit()
        return json.dumps({"deleted":probe_id}),200
    if request.method == 'GET':
        return json.dumps({"id":str(p.id),"driver":p.type,"schema":"/probe/"+probe_id+"/schema"}),200


@app.route('/probes/<probe_id>/schema',methods=['GET'])
@jwt_required()
def show_testcase(probe_id):
     p=Probem.query.filter_by(id=int(probe_id)).first()
     if p:
          return p.doc,200,{'Content-Type': 'application/xml; charset=utf-8'}


@app.route('/probes/',methods=['POST','GET'])
@jwt_required()
def createProbe():
    if request.method == 'POST':
        p=ProbeParse()
        print request.data
        probe=p.parseTestCase(str(request.data))
        probedb=Probem(probe,str(request.data))
        db_session.add(probedb)
        db_session.commit()
        return json.dumps({"id":str(probedb.id)}), 201
    if request.method == 'GET':
        allp=Probem.query.all()
        result=[]
        for p in allp:
            e=Evidence.query.filter_by(id_probe=int(p.id)).all()
            if e and len(e)>0:
                evidencep=e[0].result
                active=True
            else:
                evidencep=False
                active=False
            result.append({"id": p.id,"type": p.type,"active": active,"status": evidencep})
        return json.dumps({"results": result}),200

@app.route('/drivers',methods=['GET'])
def list_driver():
    print "required list available drivers"
    allp=Static_Probe.query.all()
    result=[]
    for p in allp:
        result.append(p.id)
    return json.dumps({result}),200

@app.route('/drivers/<driver_id>',methods=['GET'])
def get_driver(driver_id):
    print "required list available drivers"
    allp=Static_Probe.query.all(driver_id)
    if not allp:
        return json.dumps({"message":"resource not found"}),404
    result=[]
    for p in allp:
        result.append(p.id)
    return json.dumps({result}),200

@app.route('/users',methods=['GET'])
@jwt_required()
def getUser():
    print User.query.all()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}



@app.route('/api/resource',methods=['GET'])
@jwt_required()
def get_resource():
   return json.dumps({'success':str(g.user.email)}), 200, {'ContentType':'application/json'}





if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)
