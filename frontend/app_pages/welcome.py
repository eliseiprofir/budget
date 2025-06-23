import streamlit as st


def welcome_page():
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        st.title("👋 Welcome to Budget Management System")
        st.subheader("A Full-Stack Financial Solution")
        
        st.info("👨‍💻 **Portfolio Project by Elisei Profir**")
        
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
        
        st.warning("""
        #### 🔒 Secure & Private
        
        Your financial data stays private with our secure authentication system.
        """)

        st.markdown("""
        #### 📊 Powerful Analytics
        
        Gain insights with monthly, yearly, and historical reports to optimize your spending habits.
        """)
        
        st.success("""
        #### 💯 Completely Free & Open Source
        
        Enjoy all features at no cost -- we believe financial management should be accessible to everyone!
        """)
        
        st.markdown("#### 🚀 Get Started Today!")
        
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
        
        st.markdown("#### 🔗 Useful app links")
        st.markdown("Backend / Django REST Framework: https://api.elisei.pro")
        st.markdown("Frontend / Streamlit App: https://app.elisei.pro")
        st.markdown("Full documentation is available on the project's GitHub repository: https://github.com/eliseiprofir/budget")
        
        st.markdown("#### 🧐 Demo acount")
        st.markdown("- Username: demo@demo.com")
        st.markdown("- Password: demo")
        st.markdown("*Note: This account is created to see the application with random data, for demonstration purposes.*")

        st.markdown("#### 📧 Contact")
        st.markdown("Email: contact@elisei.pro")
        st.markdown("GitHub Profile: https://github.com/eliseiprofir")
        st.markdown("LinkedIn Profile: https://www.linkedin.com/in/eliseiprofir/")
