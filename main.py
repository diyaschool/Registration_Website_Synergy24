from flask import Flask, redirect, url_for, request, render_template
import smtplib
from email.message import EmailMessage

app=Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def main():
    return render_template("main.html")

@app.route('/check', methods=["POST", "GET"])
def check():
    person = request.form['class'].lower()
    print(person)
    if person == 'parent':
        return redirect(url_for('parent'))
    else:
        return redirect(url_for('visitor'))

@app.route('/parent', methods=["POST", "GET"])
def parent():
    return render_template("parent_form.html")

@app.route('/visitor', methods=["POST", "GET"])
def visitor():
    return render_template("visitor_form.html")

@app.route('/sent_p', methods=["POST", "GET"])
def sent_p():
    email=request.form.get("email")
    s_name=request.form.get("s_name")
    p_name=request.form.get("p_name")
    class_=request.form.get("class")
    section=request.form.get("section")
    p_o_no=request.form.get("o_no")
    if email in open('parent_data.csv').read():
        return render_template('error.html')
    else:
        data=f"{p_name}, {s_name}, {email}, {class_}{section}, {p_o_no}" + "\n"
        with open('parent_data.csv', 'a') as file:
            file.write(str(data))
            file.close()

        EMAIL_ADDRESS = 'info@diyaschool.com'
        EMAIL_PASSWORD = 'info123456'
        msg = EmailMessage()
        msg['Subject'] = 'Thank you for registering.'
        msg['From'] = 'pati02susan@gmail.com'
        msg['To'] = email
        msg.set_content(f'''Dear {p_name},
Thank you for visiting Synergy 2023-24. Please use the attached link to acces the floor plan to navigate around the school.
Show this email at the registration desk to get stamped for entry.
http://bit.ly/floorplan_synergy24
Best regards,
Team Diya
    ''')
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            return render_template("thankyou.html", p_name=p_name)


@app.route('/sent_v', methods=["POST", "GET"])
def sent_v():
    v_email=request.form.get("v_email")
    v_name=request.form.get("v_name")
    o_name=request.form.get("o_name")
    o_no=request.form.get("o_no")
    how=request.form.get("how")
    if v_email in open('visitor_data.csv').read():
        return render_template('error.html')
    else:
        data_v=f"{v_name}, {v_email}, {o_name}, {o_no}, {how}" + "\n"
        with open('visitor_data.csv', 'a') as file:
            file.write(str(data_v))
            file.close()

        EMAIL_ADDRESS = 'diyazoom5@gmail.com'
        EMAIL_PASSWORD = 'come_hack_me'
        msg = EmailMessage()
        msg['Subject'] = 'Thank you for registering.'
        msg['From'] = 'diyazoom5@gmail.com'
        msg['To'] = v_email
        msg.set_content(f'''Dear {v_name},
Thank you for visiting Synergy 2023-24. Please use the attached link to acces the floor plan to navigate around the school.
Show this email at the registration desk to get stamped for entry.
http://bit.ly/floorplan_synergy24
Best regards,
Team Diya
    ''')
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            return render_template("thankyou.html", v_name=v_name)


if __name__ == '__main__':
    app.run(debug=True)
