import wifi_connect
#連線WIFI
wifi_connect.connect()
#顯示IP位址
print("IP位址:", wifi_connect.get_ip()) 

#測試外部網路
if wifi_connect.test_internet():
    print("外部網路可連線")
else:
    print("外部網路無法連線")
    