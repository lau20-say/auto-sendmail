import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox

# Thông tin đăng nhập email và cài đặt SMTP
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Hàm gửi email
def send_email(recipient, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
        print("Email sent successfully!")
        server.quit()
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Biến để theo dõi số lần gửi
send_count = 0

# Hàm tự động gửi email liên tục
def auto_send_email():
    global send_count
    max_send_count = int(max_send_entry.get())
    recipient = recipient_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", tk.END)

    # Kiểm tra nếu số lần gửi đã đạt tới giới hạn
    if send_count < max_send_count:
        if send_email(recipient, subject, body):
            send_count += 1
            count_label.config(text=f"Emails Sent: {send_count}/{max_send_count}")
            # Đặt thời gian chờ giữa các lần gửi (1 giây trong ví dụ này)
            root.after(1000, auto_send_email)
        else:
            messagebox.showerror("Error", "Failed to send email.")
    else:
        messagebox.showinfo("Done", "Completed the email sending process.")

# Tạo giao diện với Tkinter
root = tk.Tk()
root.title("Automatic Email Sender")

# Trường nhập email người nhận
tk.Label(root, text="Recipient Email:").grid(row=0, column=0, padx=10, pady=5)
recipient_entry = tk.Entry(root, width=40)
recipient_entry.grid(row=0, column=1, padx=10, pady=5)

# Trường nhập tiêu đề email
tk.Label(root, text="Email Subject:").grid(row=1, column=0, padx=10, pady=5)
subject_entry = tk.Entry(root, width=40)
subject_entry.grid(row=1, column=1, padx=10, pady=5)

# Trường nhập nội dung email
tk.Label(root, text="Email Body:").grid(row=2, column=0, padx=10, pady=5)
body_text = tk.Text(root, height=10, width=40)
body_text.grid(row=2, column=1, padx=10, pady=5)

# Trường nhập giới hạn số lần gửi
tk.Label(root, text="Max Send Count:").grid(row=3, column=0, padx=10, pady=5)
max_send_entry = tk.Entry(root, width=10)
max_send_entry.insert(0, "5")  # Giá trị mặc định là 5 lần gửi
max_send_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

# Nút để bắt đầu quá trình tự động gửi
send_button = tk.Button(root, text="Start Sending", command=auto_send_email)
send_button.grid(row=4, column=1, padx=10, pady=10, sticky='e')

# Nhãn hiển thị số lần gửi
count_label = tk.Label(root, text="Emails Sent: 0/5")
count_label.grid(row=5, column=1, padx=10, pady=5, sticky='e')

root.mainloop()
