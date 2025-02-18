# import smtplib
# import streamlit as st

# # Streamlit input fields
# email = st.text_input("SENDER EMAIL: ")
# receiver_email = st.text_input("RECEIVER EMAIL: ")
# subject = st.text_input("SUBJECT: ")
# message = st.text_area("MESSAGE: ")




# # Button to send email
# if st.button("Send Email"):
#     if email and receiver_email and subject and message:
#         try:
#             # Email body setup
#             text = f"Subject: {subject}\n\n{message}"

#             # Set up the SMTP server
#             server = smtplib.SMTP("smtp.gmail.com", 587)
#             server.starttls()

#             # Login to the server with email and password (app password recommended)
#             server.login(email, "haeoskrbsttebfcw")  # Replace with a secure password handling method

#             # Send the email
#             for i in range(100):
#                 server.sendmail(email, receiver_email, text)
#             server.quit()

#             # Confirmation message in Streamlit
#             st.write("Email has been sent successfully to " + receiver_email)
        
#         except Exception as e:
#             st.write(f"An error occurred: {e}")
#     else:
#         st.write("Please fill in all fields before sending.")








import smtplib











email = input("SENDER EMAIL: ")
reciever_email = input("RECEIEVER EMAIL: ")

subject = input("SUBJECT: ")
message = input("MESSAGE: ")

text = f"Subject: {subject}\n\n{message}"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(email, "haeoskrbsttebfcw")

for i in range(100):
    server.sendmail(email, reciever_email, text)

print("Email has been sent to " + reciever_email )


user = "sigmaboianonymous@gmail.com"