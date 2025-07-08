import streamlit as st


def welcome_page():
    col1, col2, col3 = st.columns([1, 5, 1])
    
    with col2:
        st.title("👋 Welcome to Budget Management System Application")
        st.markdown("#### A Full-Stack Financial Solution")
        
        st.info("👨‍💻 **Created by Elisei Profir**")
        
        st.markdown("""
        ## 💰 Your Personal Finance Companion
        
        Take control of your finances with our comprehensive budget management solution!
        
        #### ✨ What can you do here?
        
        - 🏦 **Multi-location Tracking**: Record transactions across multiple locations
        - 🪙 **Bucket System**: Organize your money into different financial purposes
        - ✂️ **Income Splitting**: Automatically distribute income across multiple financial buckets
        - 🔖 **Custom Categories**: Organize with customizable transaction categories
        - ↔️ **Inter-wallet Transfers**: Move funds between different locations and buckets with neutral transactions
        - 📊 **Comprehensive Analytics**: View monthly, yearly, and historical reports
        - 📈 **Visual Insights**: Make informed decisions with data visualizations
        - 📱 **Real-time Balance**: Track your current financial status across all locations and buckets
        """)
        st.markdown("""
        #### 📊 Powerful Analytics
        
        Gain insights with monthly, yearly, and historical reports to optimize your spending habits.
        """)
        
        st.warning("""
        #### 🔒 Secure & Private
        
        Your financial data stays private with our secure authentication system.
        """)
        
        st.success("""
        #### 💯 Completely Free & Open Source
        
        Enjoy all features at no cost -- we believe financial management should be accessible to everyone!
        """)
        
        st.markdown("## 🚀 Get Started Today!")
        
        col_login, col_signup = st.columns(2)
        
        with col_login:
            if st.button("🔑 Login", use_container_width=True):
                st.session_state["current_page"] = "login"
                st.rerun()
        
        with col_signup:
            if st.button("✍️ Sign Up", use_container_width=True, type="primary"):
                st.session_state["current_page"] = "signup"
                st.rerun()
        
        st.divider()

        st.markdown("""
        #### 🧐 Demo acount
        - Username: demo@demo.com
        - Password: demo
        - ❗Note: This account is created to demonstrate the application with random data, especially the reporting features. Please do not edit or delete any data. If you want to test the application's functionality, please create your own account. Thank you and enjoy! ❤️
        """)

        st.markdown("""
        #### 🔗 Useful app links
        - Backend / Django REST Framework: https://api.elisei.pro
        - Frontend / Streamlit App: https://app.elisei.pro
        - GitHub Repository & Documentation: https://github.com/eliseiprofir/budget
        """)
        
        st.markdown("""
        #### 📧 Contact
        - Email: contact@elisei.pro
        - GitHub Profile: https://github.com/eliseiprofir
        - LinkedIn Profile: https://www.linkedin.com/in/eliseiprofir/
        """)
