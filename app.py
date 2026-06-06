from flask import Flask, request, render_template_string
import requests
import time
import os

app = Flask(__name__)

# तेरा ताज़ा VIP पास (बैकग्राउंड पिंग के लिए)
ACTIVE_SSQID = "6a246501dd713"

# हैकर थीम वाला वेब पेज
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Sujeet VIP Caller</title>
    <meta name="viewport" content="width=device-width, initial-width=1">
    <style>
        body { font-family: 'Courier New', Courier, monospace; background-color: #0d0d0d; color: #00ff00; text-align: center; padding: 20px; }
        .container { background: #1a1a1a; padding: 25px; border-radius: 12px; display: inline-block; box-shadow: 0px 0px 20px #00ff00; max-width: 400px; width: 100%; border: 1px solid #00ff00; }
        h2 { margin-top: 0; text-shadow: 0px 0px 10px #00ff00; }
        input { margin: 10px 0; padding: 12px; width: 90%; border-radius: 5px; border: 1px solid #00ff00; background: #000; color: #00ff00; font-weight: bold; outline: none; }
        input:focus { box-shadow: 0px 0px 8px #00ff00; }
        button { background: #00ff00; color: #000; border: none; padding: 15px; width: 96%; font-size: 18px; font-weight: bold; border-radius: 5px; cursor: pointer; margin-top: 15px; transition: 0.3s; }
        button:hover { background: #00cc00; box-shadow: 0px 0px 15px #00ff00; }
        .result { margin-top: 20px; text-align: left; background: #000; padding: 15px; border-radius: 5px; border: 1px dashed #00ff00; font-size: 14px; overflow-x: auto; }
        .footer { margin-top: 20px; font-size: 12px; color: #555; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🚀 SaleSquared VIP</h2>
        <form action="/call" method="POST">
            <input type="text" name="ssqid" value="{{ active_ssqid }}" placeholder="👉 Enter SSQID" required><br>
            <input type="text" name="confid" placeholder="👉 Enter Live CONFID" required><br>
            <input type="text" name="num1" placeholder="📞 Enter 1st Number" required><br>
            <input type="text" name="num2" placeholder="📞 Enter 2nd Number" required><br>
            <button type="submit">🔥 FIRE BOTH CALLS</button>
        </form>
        {% if result %}
        <div class="result">
            <b>Server Response:</b><br><br>
            <pre>{{ result }}</pre>
        </div>
        {% endif %}
        <div class="footer">Made by SM ⚡</div>
    </div>
</body>
</html>
"""

def fire_call(phone_number, ssqid, confid):
    url = "https://app.salesquared.io/src/ajax_req.php"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": f"ssqid={ssqid}"
    }
    
    raw_num = str(phone_number).strip()
    if not raw_num.startswith("91"):
        raw_num = f"91{raw_num}"
    if not raw_num.endswith("-c"):
        formatted_number = f"{raw_num}-c"
    else:
        formatted_number = raw_num
        
    payload = {
        "confid": confid,
        "action": "add-phone", 
        "number": formatted_number,
        "ssqid": ssqid
    }
    
    try:
        res = requests.post(url, json=payload, headers=headers)
        return res.text
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, result="", active_ssqid=ACTIVE_SSQID)

@app.route('/call', methods=['POST'])
def make_call():
    global ACTIVE_SSQID
    ssqid = request.form.get('ssqid').strip()
    confid = request.form.get('confid').strip()
    num1 = request.form.get('num1').strip()
    num2 = request.form.get('num2').strip()
    
    ACTIVE_SSQID = ssqid # सेशन ज़िंदा रखने के लिए नया पास सेव कर लिया
    
    res1 = fire_call(num1, ssqid, confid)
    time.sleep(2) # 2 सेकंड का गैप
    res2 = fire_call(num2, ssqid, confid)
    
    final_result = f"🎯 Number 1 ({num1}):\n{res1}\n\n🎯 Number 2 ({num2}):\n{res2}"
    return render_template_string(HTML_TEMPLATE, result=final_result, active_ssqid=ACTIVE_SSQID)

@app.route('/ping')
def ping():
    global ACTIVE_SSQID
    url = "https://app.salesquared.io/dashboard"
    headers = {
        "Cookie": f"ssqid={ACTIVE_SSQID}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        requests.get(url, headers=headers, timeout=10)
        return "Pinged SaleSquared! Session is Alive. 🟢"
    except:
        return "Render is Alive! 🟡"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

