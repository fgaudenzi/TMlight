from flask import Flask, json, request,abort,g, render_template, redirect, url_for
from testmanager.database import db_session, init_db
from testmanager.model.user import User
from testmanager.model.probem import Probem
from testmanager.tools.probeParser import ProbeParse
from testmanager.model.av_probe import Static_Probe
from testmanager.tools.probe_runner import runner_p
from testmanager.model.evaluation import Evidence
import sys
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'trentatre trentini'


def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(email=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True





@app.route('/login')
def log_in():
    return render_template('login.html')

@app.route('/api/token')
@auth.login_required
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



@app.route('/probe/<probe_id>/evidences/',methods=['GET'])
@auth.login_required
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


@app.route('/app',methods=['GET'])
@auth.login_required
def home():
    return render_template('home.html')


@app.route('/probe/<probe_id>/run',methods=['POST','GET'])
@auth.login_required
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
@auth.login_required
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
@auth.login_required
def show_testcase(probe_id):
     p=Probem.query.filter_by(id=int(probe_id)).first()
     if p:
          return p.doc,200,{'Content-Type': 'application/xml; charset=utf-8'}


@app.route('/probes/',methods=['POST'])
@auth.login_required
def createProbe():
    if request.method == 'POST':
        p=ProbeParse()
        print request.data
        probe=p.parseTestCase(str(request.data))
        probedb=Probem(probe,str(request.data))
        db_session.add(probedb)
        db_session.commit()
        return json.dumps({"id":str(probedb.id)}), 201


@app.route('/drivers/',methods=['GET'])
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
def getUser():
    print User.query.all()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}



@app.route('/api/resource')
@auth.login_required
def get_resource():
   return json.dumps({'success':str(g.user.email)}), 201, {'ContentType':'application/json'}


@app.errorhandler(401)
def custom_401():
    a=request_wants_json()
    return "",404
@auth.error_handler
def auth_error():
    a=request_wants_json()
    if(a):
        return "",403
    else:
         try:
            return redirect(url_for('log_in'))
         except Exception,e:
             print str(e)
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)