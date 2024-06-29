import streamlit as st
import streamlit_authenticator as stauth
from sqlalchemy import text
import yaml
import time
import re
from yaml.loader import SafeLoader
##from utils.isdef import is_variable_defined

@st.experimental_fragment
def delete():                
                name = st.text_input("Enter the name of the book")
                btn = st.button("query")
                if btn:
                    df = conn.query(f'SELECT * from books where name = "{name}";', ttl=10)
                    st.write(df)
                num=st.number_input("Enter the number of the deleted books",value = "min",step=1,min_value=0,max_value=100)
                location = st.text_input("Enter the location of the book")
                is_clicked4 = st.button("Delete")
                if is_clicked4:
                        thissql=f"Delete from books where name = '{name}' and location = '{location}' and is_borrowed = 'No' LIMIT {num}"
                        with conn.session as s:
                            s.execute(text(thissql))
                            s.commit()
                        st.write("done")      

@st.experimental_fragment
def add():
                name = st.text_input("Enter the name of the book")
                btn = st.button("query")
                if btn:
                    df = conn.query(f'SELECT * from books where name = "{name}";', ttl=10)
                    st.write(df)
                num=st.number_input("Enter the number of the added books",value = "min",step=1,min_value=0,max_value=100)
                cls = st.text_input("Enter the class of the book")
                press = st.text_input("Enter the press of the book")
                writer = st.text_input("Enter the writer of the book")
                location = st.text_input("Enter the location of the book")
                is_clicked4 = st.button("Add")
                if is_clicked4:
                        for _ in range(0,num):
                            thissql=f"Insert into books (name,class,press,writer,location) values ('{name}','{cls}','{press}','{writer}','{location}')"
                            with conn.session as s:
                                s.execute(text(thissql))
                                s.commit()
                        st.write("done")

@st.experimental_fragment
def correct():
                name = st.text_input("Enter the name of the book")
                df = conn.query(f'SELECT * from books where name = "{name}";', ttl=30)
                if df.empty:
                    st.write("Book not Found")
                else:
                    st.write(df)
                    idx= st.number_input("Object to be Corrected",value=0,step=1)
                    cls = st.text_input("Enter the class of the book")
                    press = st.text_input("Enter the press of the book")
                    writer = st.text_input("Enter the writer of the book")
                    location = st.text_input("Enter the location of the book")
                    is_clicked2 = st.button("Correct")
                    if is_clicked2:
                        thissql=f"update books SET class = '{cls}',press = '{press}',writer = '{writer}',location = '{location}' WHERE id = '{idx}'"
                        with conn.session as s:
                            s.execute(text(thissql))
                            s.commit()
                        st.write("done")  

st.sidebar.title('LibManageSys')
add_selectbox = st.sidebar.selectbox(
    "Choose your identity",
    ("Reader", "Librarian")
)

     
        
if add_selectbox == "Reader":
    temp = add_selectbox
    st.title('Ciallo～(∠・ω< )⌒★')
    with open('../reader.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )
    placeholder = st.empty()
    with placeholder.container():
         authenticator.login()
    if st.session_state["authentication_status"]:
        placeholder.empty()
        usage = st.sidebar.selectbox(  
                label=" ",                              #################################to be dev
                options=("Certificate","Borrow", "Return"),
                label_visibility="collapsed"
            )  
        authenticator.logout(location="sidebar")
        st.write(f'Welcome *{st.session_state["name"]}*')
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.001)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
###################################################################
        # Initialize connection.
        conn = st.connection('mysql', type='sql')
        ###############BUILDIHNG
        if usage == "Certificate":
            st.write("check certificate status")
            id0=st.number_input("Enter the id to certify",value = 1,step=1)
            if id0:
                df = conn.query(f'SELECT * from readers WHERE id={id0}', ttl=30)
                st.write(df)
                if (df["is_cert"] == 'N').item():
                    st.write("apply for a library certificate")
                    reason=st.text_input("Description")
                    is_clicked0 = st.button("Apply")
                    if is_clicked0:
                        thissql=f"insert into certificate (readerid,description) values ({id0},'{reason}')"
                        with conn.session as s:
                            s.execute(text(thissql))
                            s.commit()            


        elif usage == "Borrow":
            st.write("Borrow a book")
            name =st.text_input("Enter the name of the book")
            if name:
                df=conn.query(f'SELECT * from books WHERE name="{name}"', ttl=30)
                st.write(df)
            id2=st.number_input("Enter your student id",value=0,step=1)
            if id2:
                df1=conn.query(f'SELECT * from readers WHERE id={id2}', ttl=30)
                if (df1["is_cert"] == 'N').item():
                    st.write("You are not certified")
                else:
                    id1=st.number_input("Enter the book id to borrow",value=0,step=1)
                    is_clicked1 = st.button("Borrow")
                    if is_clicked1:
                        thissql=f"update books set is_borrowed = 'Yes' where id={id1}"
                        thatsql=f"insert into record (bookid,readerid,type) values ({id1},{id2},'borrow')"
                        with conn.session as s:
                            s.execute(text(thissql))
                            s.execute(text(thatsql))
                            s.commit()
            
        elif usage == "Return":
            st.write("Return a book")
            name =st.text_input("Enter the name of the book")
            df=conn.query(f'SELECT * from books WHERE name="{name}"', ttl=30)
            if df.empty:
                st.write("Book not Found")
            else:
                st.write(df)
                id2=st.number_input("Enter your student id",value=0,step=1)
                id1=st.number_input("Enter the book id to return",value=0,step=1)
                is_clicked2 = st.button("Return")
                if is_clicked2:
                    thissql=f"update books set is_borrowed = 'No' where id={id1}"
                    thatsql=f"insert into record (bookid,readerid,type) values ({id1},{id2},'return')"
                    with conn.session as s:
                        s.execute(text(thissql))
                        s.execute(text(thatsql))
                        s.commit()
        ########################
        # Perform query.
        #df = conn.query('SELECT * from mytable;', ttl=30)
        # Print results.
        #for row in df.itertuples():
        #  st.write(f"{row.name} has a :{row.pet}:")
###################################################################            
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

elif add_selectbox == "Librarian":
    temp = add_selectbox
    st.title(' 孩子們，其實那天我肘開了飛機門')
    with open('../librarian.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )
    placeholder = st.empty()
    with placeholder.container():
         authenticator.login()
    if st.session_state["authentication_status"]:
        placeholder.empty()  
        usage1 = st.sidebar.selectbox(
                label=" ",                                #################################to be dev
                options=("Certify","Books", "Readers","Records"),
                label_visibility="collapsed"
            ) 
        authenticator.logout(location="sidebar")
        st.write(f'Welcome *{st.session_state["name"]}*')
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.001)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
###################################################################
        # Initialize connection.
        conn = st.connection('mysql', type='sql')

        # Perform query.
        #df = conn.query('SELECT * from mytable;', ttl=30)

        ####BUILDING BUILT at 4/5 2:38
        if usage1 == "Certify":
            st.write("New Application")
            df = conn.query('SELECT * from certificate WHERE is_passed = "No";', ttl=30)
            st.write(df)
            if not df.empty: 
                who=st.number_input("Enter the id to certify",value=0,step=1)
                is_clicked = st.button("Certify")
                if is_clicked:
                    thissql=f"update certificate SET is_passed = 'Yes' WHERE id = {who}"
                    with conn.session as s:
                        s.execute(text(thissql))
                        s.commit()
                    st.write("done")
        
        elif usage1 == "Books":
            df = conn.query('SELECT * from books;', ttl=30)
            st.write(df)
            option = st.selectbox("Manipulate",('Correction','Add','Delete','Search'))
            if option == "Correction":
                 correct()

            elif option == "Add":
                 add()
            
            elif option == "Delete":
                 delete()
          
            elif option == "Search":
               condition=st.text_input("supplement (select * from books where ......)")
               if ';' in condition:
                    st.write("Illegal SQL command")
               else :
                    is_clicked = st.button("Execute")
                    if is_clicked:
                        df= conn.query(f"select * from books where {condition}",ttl=30)
                        st.write(df)
        #########correct books info, add books,and abstract search######## to be done ####done
        elif usage1 == "Readers":
            df = conn.query('SELECT * from readers;', ttl=30)
            st.write(df)
        elif usage1 == "Records":
            df = conn.query('SELECT * from record;', ttl=30)
            st.write(df)      
        ############

        # Print results.
        #for row in df.itertuples():
        # st.write(f"{row.name} has a :{row.pet}:")
###################################################################
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')    

