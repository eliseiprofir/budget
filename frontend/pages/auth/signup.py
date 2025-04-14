import streamlit as st
import time

def signup_page():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("Sign Up")
        st.write("Enter your details below to create an account.")
        
        name = st.text_input("Full name *")
        email = st.text_input("Email *")
        password = st.text_input("Password *", type="password")
        
        if st.button("Signup", use_container_width=True):
            if not email or not password or not name:
                st.error("Please complete all fields.")
                return

            api = st.session_state.get("auth_api")
            response = api.signup(name=name, email=email, password=password)
            
            if isinstance(response, dict):
                api.login(email=email, password=password)
                if api.is_authenticated():
                    st.session_state["authenticated"] = True
                    st.success("Account created successfully!")
                    time.sleep(1)
                    st.success("Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Account created but login failed. Please try logging in manually.")
            elif "email already exists" in response:
                st.error("Email already exists. Please use a different email.")
            else:
                st.error(f"Failed to create account: {response}")

        st.markdown("""
        ---
        Already have an account?
        """)

        if st.button("Log in"):
            st.session_state["current_page"] = "login"
            st.rerun()
