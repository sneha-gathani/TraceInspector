lines = ['Method > 1 com.flurry.sdk.fj.onReceive(com.flurry.sdk.fj@238792873,com.ovuline.pregnancy.application.PregnancyApplication@242826915,android.content.Intent@202251518<action=android.net.conn.CONNECTIVITY_CHANGE><package=null><component=null><type=null><filter_hashcode=-1172645946><networkInfo=[type: WIFI[] state: CONNECTED/CONNECTED reason: (unspecified) extra: "WiredSSID" failover: false available: true roaming: false metered: false]><networkType=1><inetCondition=0><extraInfo="WiredSSID"><umd_Intent_key=3>) 2473808']
count = 0
i = 0
for k in lines[i]:
    if(k.isspace()):
        count = count + 1
if(count > 4):
	s = 0
	tempLine = ""
	remainingArg = lines[i].split(" ")
	for k in range(0, 3):
		tempLine = tempLine + remainingArg[k] + " "
	ttemp = ""
	for k in range(3, len(remainingArg) - 1):
		ttemp = ttemp + remainingArg[k]
	ttemp.replace(" ", "")
	tempLine = tempLine + ttemp + " " + remainingArg[-1]
	lines[i] = tempLine