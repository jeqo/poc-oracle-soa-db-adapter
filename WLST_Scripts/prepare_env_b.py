import os
import time

from java.io import FileInputStream
	 
propInputStream = FileInputStream("prepare_env_b.properties")
props = Properties()
props.load(propInputStream)

connect(props.get("admin.username"), props.get("admin.password"), props.get("admin.url"))

edit()
startEdit()

dsName = props.get("datasource.name")

try:
	cd('/')
	cmo.createJDBCSystemResource(dsName)
	cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName)
	cmo.setName(dsName)
	cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName )
	set('JNDINames',jarray.array([String('jdbc/' + dsName )], String))
	cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName )
	cmo.setUrl(props.get("datasource.url"))
	cmo.setDriverName( props.get("datasource.driverclass") )
	cmo.setPassword(props.get("datasource.password"))
	cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCConnectionPoolParams/' + dsName )
	cmo.setTestTableName(props.get("datasource.testquery"))
	cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName )
	cmo.createProperty('user')
	cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/user')
	cmo.setValue(props.get("datasource.username"))
	cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName )
	cmo.createProperty('databaseName')
	cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/databaseName')
	cmo.setValue(props.get("datasource.databasename"))
	cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName )
	cmo.setGlobalTransactionsProtocol('OnePhaseCommit')
	cd('/SystemResources/' + dsName )
	set('Targets',jarray.array([ObjectName('com.bea:Name=' + props.get("datasource.target") + ',Type=Server')], ObjectName))
	save()
	activate()
	print 'Data source ' + dsName + ' configured'
except BeanAlreadyExistsException:
	print 'Error: '+dsName+' BeanAlreadyExists...'
	cancelEdit('y')

oracleHome = os.environ.get("ORACLE_HOME")
appPath= oracleHome + '/soa/connectors/DbAdapter.rar'
planPath=oracleHome + '/soa/connectors/DbAdapterPlan.xml'

CFName=props.get("eis.connfactname")
moduleOverrideName='DbAdapter.rar'
moduleDescriptorName='META-INF/weblogic-ra.xml'

def makeDeploymentPlanVariable(wlstPlan, name, value, xpath, origin='planbased'):
	while wlstPlan.getVariableAssignment(name, moduleOverrideName, moduleDescriptorName):
		wlstPlan.destroyVariableAssignment(name, moduleOverrideName, moduleDescriptorName)
	while wlstPlan.getVariable(name):
		wlstPlan.destroyVariable(name)
	variableAssignment = wlstPlan.createVariableAssignment( name, moduleOverrideName, moduleDescriptorName )
	variableAssignment.setXpath( xpath )
	variableAssignment.setOrigin( origin )
	wlstPlan.createVariable( name, value )
		
def main():
	connect(props.get("admin.username"), props.get("admin.password"), props.get("admin.url"))
	edit()
	try:
		startEdit()
		planPath_1 = get('/AppDeployments/DbAdapter/PlanPath')
		
		if (planPath_1):
			planPath = planPath_1
			print '__ Using plan ' + planPath_1
					
		myPlan = loadApplication(appPath, planPath, 'true')
		print '___ BEGIN change plan'
		makeDeploymentPlanVariable(myPlan, 'ConnectionInstance_' + CFName +'_JNDIName_abc123XXX', CFName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="'+ CFName + '"]/jndi-name')
		makeDeploymentPlanVariable(myPlan, 'ConfigProperty_xADataSourceName_'+ dsName +'_abc123XXX', 'jdbc/'+dsName , '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="'+ CFName + '"]/connection-properties/properties/property/[name="xADataSourceName"]/value')
		print '___ DONE change plan'
		myPlan.save();
		save();
		activate(block='true');
		cd('/AppDeployments/DbAdapter/Targets');

		redeploy('DbAdapter', planPath,targets=cmo.getTargets());
		print 'EIS Connection factory ' + CFName + ' using ' + dsName + ' configured';
	except Exception, e:
		print e
		stopEdit('y')
			   
main()


