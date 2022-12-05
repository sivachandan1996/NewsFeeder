import News_feeder_streamlit as ns
import streamlit as st
import random


st.title("News scrapping of public figures from Google News")
input= st.container()
with input:
    search_item = st.text_input("Enter the name of Public Figure")
    if search_item:
        url =  ns.build_url(search_item=search_item)
        if url is not False:
            st.success('URL Build Sucessfully', icon="✅")
            st.code(f"{url}")
            st.write("")
            st.info("Getting the HTML Page",icon="ℹ️")
            html = ns.get_html(url,search_item=search_item)
            if html is not False:
                st.success('Obtained the HTML Page', icon="✅")
                st.write("")
                st.info("Sracpping the page for the News",icon='ℹ️')
                email_html_body = ns.main_content(html=html,search_item=search_item)
                if email_html_body is not False:
                    st.success('Completed Scrapping Process', icon="✅")
                    st.write("")
                    recipient_email = st.text_input("Enter your E-mail 📧")
                    if recipient_email:
                        st.info("Sending the mail",icon='ℹ️')
                        status = ns.mail(email_html_body=email_html_body,\
                            to_mail=recipient_email,search_item=search_item)
                        if status is True:
                            st.success('Mail 📧 Sent Sucesfully', icon="✅")
                            choice = random.randint(1,2)
                            if choice == 1:
                                st.snow()
                            if choice == 2:
                                st.balloons()
                     
                        else:
                            st.error("Couldnt send the mail", icon="🚨")    

                elif email_html_body is False:
                    st.error(f"Couldnt Scrap the Google News for {search_item}")
                    st.warning('Check the Spelling', icon="⚠️")
            elif html is False:
                st.error('couldnt get HTML', icon="🚨")

        elif url is False:
            st.error('Some thing went wrong couldn\'t build URL', icon="🚨")

