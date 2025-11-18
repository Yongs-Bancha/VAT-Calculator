from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>คำนวณภาษี VAT 7%</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 500px;
            width: 100%;
        }
        
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 30px;
            font-size: 28px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }
        
        input[type="number"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .radio-group {
            display: flex;
            gap: 20px;
            margin-top: 10px;
        }
        
        .radio-option {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        input[type="radio"] {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .result {
            margin-top: 30px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 5px solid #667eea;
        }
        
        .result h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 22px;
        }
        
        .result-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .result-item:last-child {
            border-bottom: none;
            font-weight: 700;
            font-size: 18px;
            color: #667eea;
            margin-top: 10px;
        }
        
        .result-label {
            color: #666;
        }
        
        .result-value {
            color: #333;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧾 คำนวณภาษี VAT 7%</h1>
        
        <form method="POST">
            <div class="form-group">
                <label for="amount">จำนวนเงิน (บาท):</label>
                <input type="number" id="amount" name="amount" step="0.01" required 
                       value="{{ amount if amount else '' }}" placeholder="กรอกจำนวนเงิน">
            </div>
            
            <div class="form-group">
                <label>ประเภทการคำนวณ:</label>
                <div class="radio-group">
                    <div class="radio-option">
                        <input type="radio" id="exclude" name="calc_type" value="exclude" 
                               {% if calc_type == 'exclude' or not calc_type %}checked{% endif %}>
                        <label for="exclude">ยังไม่รวม VAT</label>
                    </div>
                    <div class="radio-option">
                        <input type="radio" id="include" name="calc_type" value="include"
                               {% if calc_type == 'include' %}checked{% endif %}>
                        <label for="include">รวม VAT แล้ว</label>
                    </div>
                </div>
            </div>
            
            <button type="submit">คำนวณ</button>
        </form>
        
        {% if result %}
        <div class="result">
            <h2>ผลการคำนวณ</h2>
            <div class="result-item">
                <span class="result-label">ราคาก่อน VAT:</span>
                <span class="result-value">{{ "฿{:,.2f}".format(result.price_before_vat) }}</span>
            </div>
            <div class="result-item">
                <span class="result-label">ภาษี VAT 7%:</span>
                <span class="result-value">{{ "฿{:,.2f}".format(result.vat_amount) }}</span>
            </div>
            <div class="result-item">
                <span class="result-label">ราคารวม VAT:</span>
                <span class="result-value">{{ "฿{:,.2f}".format(result.price_with_vat) }}</span>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    amount = None
    calc_type = 'exclude'
    
    if request.method == 'POST':
        amount = float(request.form.get('amount', 0))
        calc_type = request.form.get('calc_type', 'exclude')
        
        if calc_type == 'exclude':
            # กรณียังไม่รวม VAT
            price_before_vat = amount
            vat_amount = amount * 0.07
            price_with_vat = amount * 1.07
        else:
            # กรณีรวม VAT แล้ว
            price_with_vat = amount
            price_before_vat = amount / 1.07
            vat_amount = price_with_vat - price_before_vat
        
        result = {
            'price_before_vat': price_before_vat,
            'vat_amount': vat_amount,
            'price_with_vat': price_with_vat
        }
    
    return render_template_string(HTML_TEMPLATE, result=result, amount=amount, calc_type=calc_type)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)