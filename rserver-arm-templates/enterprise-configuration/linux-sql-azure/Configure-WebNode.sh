#!/bin/bash

password=$1
sqlServerConnectionString=$2
aadTenant=$3
aadClientId=$4
/usr/local/bin/dotnet /usr/lib64/microsoft-r/rserver/o16n/9.1.0/Microsoft.RServer.Utils.AdminUtil/Microsoft.RServer.Utils.AdminUtil.dll -silentwebnodeinstall "$password"
