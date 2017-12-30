# !/usr/bin/python
# -*-coding: utf-8-*-

import requests, random

# 构造headers
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
	'Connection': 'keep-alive',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
}

# 建立Session
session = requests.session()

# IP代理池
ip_pools = ['115.220.3.25:808','124.235.145.162:80','61.157.198.66:8080','122.244.54.19:808','27.204.64.99:808','123.169.88.6:808','114.239.0.183:808','123.55.191.113:808','27.213.190.195:8889','171.13.37.31:808','60.173.58.133:8888','223.244.154.82:808','112.81.77.221:53281','117.43.0.84:808','183.151.40.78:808','183.151.41.64:808','175.155.247.240:808','27.222.81.255:8889','117.143.109.168:80','115.203.76.46:808','112.195.49.71:808','39.77.29.128:8889','222.95.18.165:808','112.250.198.0:8889','222.94.144.15:808','125.78.109.149:808','119.5.221.78:808','180.173.109.149:8118','27.8.60.238:8888','122.241.73.198:808','119.254.84.90:80','101.71.17.132:8081','221.229.46.15:808','222.94.148.215:808','115.202.164.117:808','115.151.5.202:808','222.122.202.175:80','27.204.86.127:808','203.115.19.247:8080','182.38.98.186:808','171.117.121.204:8080','175.155.225.219:808','113.123.18.114:808','39.71.134.28:8889','180.110.132.209:808','180.121.132.80:808','121.62.158.173:808','114.99.0.181:808','49.82.107.205:808','110.189.223.30:808','115.220.4.47:808','180.118.240.177:808','112.195.98.175:808','60.173.34.17:808','222.94.150.107:808','183.153.27.114:808','222.85.50.230:808','61.188.24.242:808','180.118.243.146:808','114.239.1.204:808','60.184.174.179:808','114.99.23.138:808','125.89.126.21:808','111.62.251.67:80','180.118.243.184:808','175.155.96.84:808','222.85.39.48:808','114.239.146.124:808','111.11.83.241:80','27.204.172.103:808','115.220.7.174:808','222.94.147.108:808','117.57.255.111:808','171.13.36.14:808','123.170.90.19:808','49.87.247.40:808','60.178.5.225:8081','180.114.216.114:808','123.163.21.68:808','113.140.25.4:81','49.76.109.2:53281','115.216.254.115:808','123.163.164.30:808','114.239.3.101:808','111.11.83.242:80','218.15.25.153:808','117.143.109.170:80','61.183.8.51:3128','113.121.39.231:808','115.213.201.0:808','122.245.71.253:808','122.192.74.83:8080','125.89.121.129:808','60.211.182.76:8080','222.89.82.220:808','112.195.154.142:808','121.62.162.32:808','180.118.242.72:808','27.46.55.55:8118','222.94.150.97:808','119.7.217.97:808','112.194.46.168:808','115.212.59.77:808','116.211.135.68:8080','106.46.71.235:808','113.123.127.213:808','118.144.54.247:8118','153.36.169.147:808','113.123.18.121:808','115.213.203.72:808','117.43.0.255:808','119.7.78.169:808','119.7.81.67:808','27.204.81.111:808','27.213.228.174:53281','60.21.132.218:63000','122.244.53.208:808','125.109.192.26:808','117.91.138.203:808','119.7.225.47:808','125.89.122.101:808','123.169.37.142:808','175.155.231.88:808','124.115.157.8:80','111.62.251.70:80','113.123.18.7:808','218.59.62.209:8888','123.169.36.83:808','180.110.134.75:808','39.73.131.77:8889','27.213.97.244:8889','60.178.175.107:8081','115.220.147.247:808','117.143.109.155:80','117.91.138.14:808','110.6.203.85:8118','120.33.247.23:808','114.232.2.182:808','59.38.241.164:808','123.169.85.89:808','61.191.41.130:80','122.228.179.178:80','218.161.28.115:8998','218.201.98.196:3128','58.221.47.190:8080','222.85.39.84:808','123.169.84.72:808','175.155.224.127:808','115.220.148.224:808','39.76.32.57:808','180.121.135.136:808','1.197.203.177:55232','1.199.194.18:808','182.87.241.70:808','115.151.5.249:808','111.76.224.243:808','182.87.242.44:808','123.169.89.76:808','58.217.255.184:1080','218.64.93.228:808','182.45.176.182:808','222.94.169.75:8888','125.116.175.156:808','123.170.255.173:808','113.124.87.220:808','61.188.24.5:808','222.129.236.24:8118','114.239.148.226:808','119.5.221.10:808','125.124.160.238:47954','58.253.153.34:808','182.138.129.84:80','120.37.198.79:808','113.123.18.77:808','121.22.216.253:8888','171.13.37.115:808','119.7.79.117:808','219.149.46.151:3128','121.62.161.136:808','180.119.65.31:808','111.62.243.64:8080','106.42.198.140:808','175.155.96.125:808','115.220.144.42:808','117.143.109.157:80','111.62.251.24:80','175.155.97.127:808','221.229.44.115:808','117.91.138.103:808','111.13.7.42:843','60.250.72.252:8080','121.205.181.201:808','113.121.46.228:808','115.220.148.104:808','222.95.22.161:808','119.186.66.100:8889','123.169.89.165:808','39.76.42.109:808','115.213.240.158:808','59.173.13.172:3128','144.255.213.230:8118','175.155.97.45:808','115.220.5.113:808','222.169.193.162:8099','182.45.178.12:8889','221.229.45.136:808','122.245.65.78:808','222.95.16.97:808','59.38.241.139:808','113.120.104.76:80','115.213.246.12:808','60.185.209.24:8998','180.110.5.1:808','115.213.202.122:808','183.131.19.233:3128','112.252.16.104:8889','112.195.101.224:808','114.239.151.108:808','27.204.168.155:808','112.86.107.240:8888','222.94.150.67:808','61.143.17.169:808','122.245.66.45:808','119.179.193.69:8889','58.221.71.126:8080','125.106.94.140:808','113.121.171.212:808','125.105.105.62:808','119.254.102.90:8080','60.167.23.177:808','114.230.219.33:808','121.10.141.149:8080','122.245.69.116:808','182.45.159.66:8889','112.252.172.145:8889','112.33.7.9:8081','61.183.8.61:3128','117.86.206.129:808','171.13.36.75:808','183.153.15.143:808','183.140.249.3:8998','221.202.251.217:8118','175.155.243.40:808','117.143.109.171:80','115.221.116.237:808','113.69.178.170:808','120.33.247.150:808','60.173.96.189:808','125.115.181.115:808','123.163.142.254:808','180.110.132.53:808','117.57.23.32:808','222.95.16.200:808','61.134.29.25:8080','112.250.213.212:8889','222.95.19.32:808','27.204.45.36:808','175.155.224.208:808','183.131.215.86:8080','180.115.173.234:808','60.184.173.237:808','61.188.24.122:808','106.42.23.201:808','117.172.79.4:8080','183.151.40.10:808','114.106.23.45:808','115.231.175.68:8081','39.76.34.40:808','114.99.18.160:808','121.234.39.229:808','123.54.232.180:808','218.26.227.108:80','27.204.117.27:808','175.155.225.147:808','171.13.37.91:808','113.206.202.29:8118','60.173.96.189:808','117.86.86.60:808','123.55.177.157:808','59.61.92.205:8118','117.35.236.175:80','153.36.10.54:808','114.238.144.155:808','123.169.89.220:808','27.204.127.23:808','175.155.226.8:808','223.71.227.242:8118','115.220.5.124:808','110.244.119.139:80','153.36.11.93:808','111.11.83.243:80','114.99.6.121:808','114.239.148.31:808','175.155.191.151:808','111.78.74.235:808','180.110.132.19:808','114.239.151.236:808','1.171.159.186:3128','114.239.249.224:808','113.123.18.207:808','125.116.174.131:808','114.99.8.57:808','125.89.126.24:808','119.7.79.147:808','60.211.60.249:8889','123.55.94.21:808','58.221.38.70:8080','222.94.149.181:808','61.188.24.106:808','125.115.182.30:808','114.230.120.244:808','221.229.45.173:808','117.143.109.167:80','222.85.50.192:808','119.185.4.39:8889','111.62.251.25:80','222.85.19.221:808','111.11.83.240:80','114.230.126.15:808','223.241.79.241:808','114.99.22.109:808','123.55.94.92:808','61.135.155.82:443','117.143.109.164:80','119.7.225.97:808','163.125.31.71:8118','114.231.242.203:808','117.43.1.227:808','106.5.7.117:808','123.163.161.172:808','123.153.115.227:808','125.89.122.19:808','1.197.198.182:808','180.118.242.120:808','125.89.121.163:808','220.174.236.211:80','182.45.130.126:808','117.28.144.22:808','222.185.148.252:808','211.143.112.138:8118','1.197.56.77:808','121.62.159.86:808','125.89.121.139:808','183.151.41.22:808','111.62.251.130:80','180.119.65.63:808','119.7.84.35:808','70.97.223.199:53281','183.186.126.154:8080','175.155.241.42:808','113.123.19.194:808','175.148.213.55:80','123.169.90.224:808','113.123.18.59:808','114.99.2.33:808','121.62.163.59:808','180.105.192.138:808','115.216.145.215:8118','180.110.134.176:808','121.205.190.107:808','122.241.73.225:808','113.244.101.108:8118','180.118.240.186:808','222.95.19.120:808','122.245.69.193:808','183.151.43.111:808','106.42.199.212:808','115.203.66.40:808','125.106.128.199:808','115.220.147.232:808','125.89.121.22:808','121.226.162.237:808','123.7.177.20:9999','114.235.81.127:808','175.155.221.115:808','117.28.146.18:808','112.194.173.138:808','114.239.148.26:808','121.61.17.36:8118','60.184.175.137:808','122.245.71.85:808','182.32.151.213:808','123.163.83.10:808','180.118.240.52:808','222.95.18.4:808','222.185.190.39:808','113.123.18.55:808','125.115.182.137:808','125.89.123.6:808','125.89.123.172:808','119.7.35.150:808','113.123.18.203:808','114.232.152.20:808','113.121.37.154:808','114.236.65.56:808','119.7.72.19:808','218.64.93.91:808','175.155.230.49:808']

proxies = {
	'http': random.choice(ip_pools)
}

# Get方法
def get(url, data = {}):
	return session.get(url, data = data, headers = headers)

# Post方法
def post(url, data = {}):
	return session.post(url, data = data, headers = headers)