import streamlit as st


def guide_page():
    st.title("📖 User Guide")
    
    st.markdown("""
    Welcome to the Budget Management System User Guide! This guide will help you understand how to use the app effectively.
    """)

    st.markdown("""
    #### 🔑 Key Concepts
    """)
    
    with st.expander("🏦 Locations", expanded=True):
        st.markdown("""
        **Locations** represent where your money is physically or virtually stored.

        - Examples: Cash, ING, Revolut, Savings account, Investment account
        - Each location tracks its own balance
        - You can transfer money between locations using neutral transactions (see more below).
        - Every transaction must have a location
        """)
    
    with st.expander("🪙 Buckets", expanded=True):
        st.markdown("""
        **Buckets** represent different purposes or categories for your money.
        
        - Examples: Economies, Investments, Necessities, Education, Donation, Fun
        - Each bucket has an **Allocation Percentage** that determines how income is distributed
        - Total allocation percentages across all buckets should equal 100%
        - Buckets help you organize your money by purpose rather than location
        - Every transaction must have a bucket
        
        **Split Income Feature**: When your bucket allocations total 100%, you can use the "Split Income" option for positive transactions. This automatically creates multiple transactions that distribute your income according to your bucket allocation percentages. For example, if you receive 1000 and have buckets set up as Education (30%), Necessities (50%), and Fun (20%), the system will automatically create three separate transactions of 300, 500, and 200 to the respective buckets. Useful for automatically allocating your salary or other regular income.
        """)
    
    with st.expander("🔖 Categories", expanded=True):
        st.markdown("""
        **Categories** help classify your transactions by type. Each category has a **Sign**:
        - **Positive**: Money coming in -- Examples: Income, Salary, Gifts, etc.
        - **Negative**: Money going out -- Examples: Expenses, Bills, Food, Car, Health, Technology, etc.
        - **Neutral**: Money moving between your locations/buckets or temporary transactions -- Examples: Transfers, Loans, etc.

        **About Neutral Transactions**: You can use them in 2 different purposes:
        1. Transfers between your own accounts or buckets. They don't affect your overall balance but change the distribution of money. For example, moving 500 from your ING account to Revolut account requires two transactions: one negative from ING and one positive to Revolut. Both transactions should use a neutral category to indicate this is just moving money around, not income or expense.
        2. Temporary transactions like loans. For example, if you borrow or lend money temporarily, these transactions won't affect your overall balance but show up on your reports.
        
        Categories help with reporting and understanding your spending patterns.
        """)
    
    st.markdown("## 📝 Common Tasks")
    
    with st.expander("🟢 How to Record Income", expanded=True):
        st.markdown("""
        0. Make sure you have a positive category created before
        1. Go to "Transaction Management" page and click on the "Add transaction" button
        2. Select a **Positive category** (Salary, Gift, etc.)
        3. Complete the rest of the fields (description, date, amount, location)
        4. You want to split income into buckets?
            - If YES: Check "Split income" to distribute across buckets according to allocation percentages. I doesn't matter the bucket selected. 
            - If NO: Leave "Split income" unchecked but select a specific bucket. The transaction will go directly to that bucket.
        5. Save the transaction
        
        **Note**: If you want to use "Split income" feature, first make sure your bucket allocation is completed (100%). You can check this in "Budget Configuration" page.
        """)
    
    with st.expander("🔴 How to Record Expenses", expanded=True):
        st.markdown("""
        0. Make sure you have a negative category created before
        1. Go to "Transaction Management" page and click on the "Add transaction" button
        2. Select a **Negative** category (Bills, Food, Car)
        3. Enter the amount as a positive number (the system will handle the negative sign)
        4. Complete the rest of the fields (description, date, location, bucket)
        5. Save the transaction
        
        **Note**: "Split income" feature is not available for expenses.
        """)
    
    with st.expander("⚪ How to Make Neutral Transactions", expanded=True):
        st.markdown("""
        All neutral transactions require **two separate transactions**, one for the source and one for the destination.
        ### Transfers between Locations/Buckets
        
        ##### Step 1: Create the outgoing transaction
        1. Select the **Neutral** category you want to use
        2. Enter the amount as a **NEGATIVE NUMBER**
        3. Select the **source location/bucket** (where money is coming from)
        4. Save the transaction
        
        ##### Step 2: Create the incoming transaction
        1. Select the same **Neutral** category as above
        2. Enter the **same amount** as a **POSITIVE NUMBER**
        3. Select the **destination location/bucket** (where money is going to)
        4. If you're transferring between buckets, select the same location as the outgoing transaction. If you're transferring between locations, select the same bucket as the outgoing transaction.
        5. Save the transaction
        
        ### Loans/Temporary Transactions
        Create a special neutral category for these kind of transactions.
        ##### If you lend money to someone
        Enter **NEGATIVE AMOUNT** on outgoing transaction (when you give it) and **POSITIVE AMOUNT** on incoming transaction (when you receive them back).
        ##### If you borrow money from someone
        Enter **POSITIVE AMOUNT** on outgoing transaction (when you take it) and **NEGATIVE AMOUNT** on incoming transaction (when you pay them back).
        """)
    
    st.info("""
    ## 🔍 Tips & Best Practices
    - **Set up your locations, buckets, and categories** in order to be able to add transactions (see "Budget Configuration" page)
    - **Complete your bucket allocation** with proper allocation percentages before using split income (see "Budget Configuration" page)
    - **Regularly review** your transactions to ensure accuracy
    - **Use consistent categories** to make your reports more meaningful
    - **Check your balances** periodically to ensure they match your actual accounts
    - **Use descriptive transaction names** to help you remember what each transaction was for
    """)

    st.warning("""
    #### ⚠️ Important Warning
    **All changes made in this system are permanent.** Please be careful when adding, editing, or deleting data. 
    There is no automatic "undo" feature, so double-check your entries before confirming them.
    """)
    
    st.success("""
    🤩 That's it! With these guidelines, you should be able to use the app efficiently and manage your finances with ease! Enjoy!
    """)

    st.write("""
    If you encounter any errors or bugs, please email us at contact@elisei.pro with as many details as possible — ideally including screenshots. We'll get back to you with a solution as soon as we can. Thank you!
    """)
