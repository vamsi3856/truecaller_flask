from flask import Flask, request, render_template
import subprocess
import re  # Add this import statement
import asyncio
from truecallerpy import search_phonenumber

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("lookup.html")


@app.route('/truecaller/', methods=['GET', 'POST'])
async def truecaller_info():
    id = "a1i0I--jiay5xFzVC6nP-uHLMkTKkCN3goLtkd3OyRhw0L13EFSTKSAi2742yK81"
    if request.method == "POST":
        phone_numbers = request.form.get("contact")  # Change request.POST to request.form
        phone_numbers_list = phone_numbers.split(',')
        num_lst=[i.strip() for i in phone_numbers_list]
        results = {}

        for phone_number in num_lst:
            i=phone_number
            if len(phone_number)==10:
                phone_number = "+1"+phone_number
            try:
                result = await search_phonenumber(phone_number,"", id)
                # print(result)
                # Check if the 'name' key exists in the result
                if 'data' in result and 'data' in result['data'] and 'name' in result['data']['data'][0]:
                    output = result['data']['data'][0]['name']
                else:
                    output="Name not available"
                
            except Exception as e:
                output = f"Error: {e}"
            results[i] = output

        context = {
            'results': results,
        }
        return render_template('result.html', **context)  # Use render_template correctly



if __name__ == '__main__':
    app.run()
