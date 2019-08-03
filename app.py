from flask import Flask,request,render_template
import azure.cosmos.cosmos_client as cosmos_client
config = {
    'ENDPOINT': 'https://pes.documents.azure.com:443/',
    'PRIMARYKEY': 'AtZKUUeFCbpfaJpfVgLuua4hwlccrx8jTrenMwixuDQpbt9QVbKuZcWBiVG64vOw3OfUYwJAlrTgSzQIgxOBuQ==',
    'DATABASE': 'pes'
}
# Initialize the Cosmos client
client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={
                                    'masterKey': config['PRIMARYKEY']})
students=client.ReadContainer('dbs/pes/colls/students')['_self']
teachers=client.ReadContainer('dbs/pes/colls/teachers')['_self']
tc=client.ReadContainer('dbs/pes/colls/tc')['_self']
assignments=client.ReadContainer('dbs/pes/colls/assignments')['_self']
student_tc=client.ReadContainer('dbs/pes/colls/student_tc')['_self']
courses=client.ReadContainer('dbs/pes/colls/courses')['_self']
app = Flask(__name__)

@app.route('/')
def list_assignments():
	list_tc=client.QueryItems(	tc,
					"SELECT * FROM server s WHERE s.teacher_id = 't_1'", 
					{'enableCrossPartitionQuery':True}
				   )
	name=[i['name'] for i in client.QueryItems(	teachers,
					"SELECT s.name FROM server s WHERE s.teacher_id = 't_1'", 
					{'enableCrossPartitionQuery':True}
				   )][0]
	ar=list()
	
	for i in list_tc:
		ar.append(i['tc_id'])
	st='\',\''.join(ar)
	print(st)
	list_ass = client.QueryItems(	assignments,
					"SELECT * FROM server s WHERE s.posted_by_to in (\'"+st+"\')", 
					{'enableCrossPartitionQuery':True}
				   )
	for item in list_ass:
		print(item["heading"])
	passer=[]
	for item in iter(list_ass):
		course =[i['course_id'] for i in client.QueryItems(	tc,
					"SELECT s.course_id FROM server s WHERE s.tc_id=\'"+item['posted_by_to']+"\'", 
					{'enableCrossPartitionQuery':True}
				   )][0]
		cname=[i['name'] for i in client.QueryItems(	courses,
					"SELECT s.name FROM server s WHERE s.course_id=\'"+course+"\'", 
					{'enableCrossPartitionQuery':True}
				   )][0]
		
		passer.append({
			'assignment_id' : item['assignment_id'],
			'heading' : item['heading'],
			'deadline' :item['deadline'],
			'max_marks' : item['max_marks'],
			'posted_on' : item['posted_on'],
			'professor' : name,
			'course' : course+' '+cname
		})
	print(passer)
	return render_template('teachers/list.html',arg=passer,len=len(passer))
@app.route('/s')
def stud():
   return render_template('students/assignment_list.html')
@app.route('/assignment/a_1')
def s():
	return "eh"
if __name__ == '__main__':
   app.run(debug = True)
