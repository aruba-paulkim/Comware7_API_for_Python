# Comware7 API for Python

### Installation
<pre>git clone https://github.com/aruba-paulkim/Comware7_API_for_Python.git
python3 -m venv Comware7_API_for_Python
cd Comware7_API_for_Python
source bin/activate
pip install -r requirements.txt</pre>


### Config
change Comware7_API.py file
<pre>...
API_BASE = "https://{COMWARE7_IP}"
API_AUTH = "YOUR_LOGIN_ID:YOUR_LOGIN_PW"
...
</pre>


### Run
<pre>python3 Comware7_API.py {add|del} acct_id acct_pw</pre>
