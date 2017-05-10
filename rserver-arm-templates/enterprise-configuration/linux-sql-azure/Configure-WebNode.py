#!/usr/bin/python

import sys
import json
import os
from collections import OrderedDict

linuxOS=sys.argv[1]
password=sys.argv[2]
aadTenant=sys.argv[3]
aadClientId=sys.argv[4]
sqlServerConnectionString=sys.argv[5]

appSettingsFilePath = "/usr/lib64/microsoft-r/rserver/o16n/9.1.0/Microsoft.RServer.WebNode/appsettings.json"
f = open(appSettingsFilePath, "r")
jsondata = f.read().decode("utf-8-sig").encode("utf-8").replace("\r\n","")
data = json.loads(jsondata, object_pairs_hook=OrderedDict)

data["ConnectionStrings"]["sqlserver"]["Enabled"] = True
data["ConnectionStrings"]["sqlserver"]["Connection"] = sqlServerConnectionString
data["ConnectionStrings"]["defaultDb"]["Enabled"] = False
data["ConnectionStrings"]["defaultDb"]["Enabled"] = False
data["BackEndConfiguration"]["Uris"]["Ranges"] =  ["http://10.0.1.0-255:12805"]

if aadTenant != "":
    data["Authentication"]["AzureActiveDirectory"]["Authority"] = "https://login.windows.net/" + aadTenant
    data["Authentication"]["AzureActiveDirectory"]["Audience"] = aadClientId
    data["Authentication"]["AzureActiveDirectory"]["Enabled"] = True

if linuxOS != "Ubuntu":
    data["Authentication"]["JWTSigningCertificate"]["Enabled"] = True
    data["Authentication"]["JWTSigningCertificate"]["StoreName"] = ""
    data["Authentication"]["JWTSigningCertificate"]["StoreLocation"] = "/usr/lib/ssl"
    data["Authentication"]["JWTSigningCertificate"]["SubjectName"] = "CN=ACCVRAIZ1,OU=PKIACCV,O=ACCV,C=ES"
else:
    data["Authentication"]["JWTSigningCertificate"]["Enabled"] = True
    data["Authentication"]["JWTSigningCertificate"]["StoreName"] = ""
    data["Authentication"]["JWTSigningCertificate"]["StoreLocation"] = "/etc/pki/tls"
    data["Authentication"]["JWTSigningCertificate"]["SubjectName"] = "C=US, O=Entrust.net, OU=www.entrust.net/CPS incorp. by ref. (limits liab.), OU=(c) 1999 Entrust.net Limited, CN=Entrust.net Secure Server Certification Authority"

f = open(appSettingsFilePath, "w")
json.dump(data, f, indent=4, sort_keys=False)
f.close()

os.system("/usr/local/bin/dotnet /usr/lib64/microsoft-r/rserver/o16n/9.1.0/Microsoft.RServer.Utils.AdminUtil/Microsoft.RServer.Utils.AdminUtil.dll -silentwebnodeinstall \"" + password + "\"")

if linuxOS != "Ubuntu":
    os.system("yum install -y epel-release")
    os.system("yum install -y nginx")
    os.system("sed -i 's#location / {#location /ping { return 200 \"hello\";#g' /etc/nginx/nginx.conf")
    os.system("systemctl start nginx")
    os.system("systemctl enable nginx")
else:
    os.system("apt-get install -y nginx")
    os.system("sed -i 's%# pass the PHP scripts%location /ping { return 200 \"hello\"; }#%g' /etc/nginx/sites-enabled/default")
    os.system("service nginx start")
    os.system("update-rc.d nginx defaults")