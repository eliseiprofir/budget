import streamlit as st


def guide_page():
    st.title("📖 User Guide")
    
    st.markdown("""
    Welcome to the Budget Management System User Guide! This guide will help you understand how to use the app effectively.
    """)

    st.markdown("""
    📲 If you're on mobile, use the **arrow** (>) in the top left corner to open the navigation bar with all pages.
    """)

    st.warning("### 🔑 Key Concepts")
    
    with st.expander("🏦 Locations", expanded=False):
        st.markdown("""
        **Locations** represent where your money is physically or virtually stored.

        - Examples: Cash, ING, Revolut, Savings account, Investment account
        - Each location tracks its own balance
        - You can transfer money between locations using neutral transactions (see more below).
        - Every transaction must have a location
        """)
    
    with st.expander("🪙 Buckets", expanded=False):
        st.markdown("""
        **Buckets** represent different purposes or categories for your money.
        
        - Examples: Economies, Investments, Necessities, Education, Donation, Fun
        - Each bucket has an **Allocation Percentage** that determines how income is distributed
        - Total allocation percentages across all buckets should equal 100%
        - Buckets help you organize your money by purpose rather than location
        - Every transaction must have a bucket
        
        **Split Income Feature**:
        - When your bucket allocations total 100%, you can use the "Split Income" option for positive transactions.
        - This automatically creates multiple transactions that distribute your income according to your bucket allocation percentages.
        - Example: if you receive 1000 and have buckets set up as Education (30%), Necessities (50%), and Fun (20%), the system will automatically create three separate transactions of 300, 500, and 200 to the respective buckets.
        - Useful for automatically allocating your salary or other regular income.
        
        💡 Tip for allocation percentages: If unsure, try: Economies (20%), Education (10%), Necessities (50%), Fun (10%), Donation (10%)
        """)
    
    with st.expander("🔖 Categories", expanded=False):
        st.markdown("""
        **Categories** help classify your transactions by type. Each category has a **Sign**:
        - **Positive**: Money coming in -- Examples: Income, Salary, Gifts, etc.
        - **Negative**: Money going out -- Examples: Expenses, Bills, Food, Car, Health, Technology, etc.
        - **Neutral**: Money moving between your locations/buckets or temporary transactions -- Examples: Transfers, Loans, etc.

        **About Neutral Transactions**: You can use them in 2 different purposes:
        1. Transfers between your own accounts or buckets. They don't affect your overall balance but change the distribution of money. For example, moving 500 from your ING account to Revolut account requires two transactions: one negative from ING and one positive to Revolut. Both transactions should use a neutral category to indicate this is just moving money around, not income or expense.
        2. Temporary transactions like loans. For example, if you borrow or lend money temporarily, these transactions won't affect your overall balance but show up on your reports.
        
        Categories help with reporting and understanding your spending patterns.
        
        💡 Tip for names: Add a prefix ("+" or 🟢), negative ("-" or 🔴) and neutral ("=" or ⚪) to differentiate between categories. It will help you find them easier when you add new transactions or filter them. You can also add prefixes to pair them with buckets/purposes (e.g. "-Necessities/Food", "-Necessities/Clothes","-Education/Books").
        """)
    
    st.error("### 🚀 Initial Setup")
    st.markdown("""
    Setting up your budget app for the first time? Follow these steps to get everything configured properly -- it will make your daily use much easier!
    """)
    
    with st.expander("Step 1: Create Your Budget Configuration", expanded=False):
        st.markdown("""
        Go to **"Budget Configuration"** page and set up:
        
        **🏦 Locations**: Add all places where you store money
        - Examples: Cash, ING, Revolut, Savings account, Investment account
        - Add every account/wallet you actually use
        
        **🪙 Buckets**: Create buckets for your money's purpose
        - Examples: Economies, Education, Necessities, Fun, Donation
        - **Important**: Set allocation percentages that total exactly 100% (this enables Split Income feature)
        
        💡 Tip for allocation percentages: If unsure, try: Economies (20%), Education (10%), Necessities (50%), Fun (10%), Donation (10%)
        
        **🔖 Categories**: Create transaction categories you'll use
        - **Positive**: +Income, +Salary, +Gift, +Bonus, etc.
        - **Negative**: -Food, -Bills, -Car, -Health, -Technology, etc.
        - **Neutral**: =Transfer, =Loan, etc.
        
        💡 Tip for names: Add a prefix ("+" or 🟢), negative ("-" or 🔴) and neutral ("=" or ⚪) to differentiate between categories. It will help you find them easier when you add new transactions or filter them. You can also add prefixes to pair them with buckets/purposes (e.g. "-Necessities/Food", "-Necessities/Clothes","-Education/Books").
        """)
    
    with st.expander("Step 2: Add Your Current Money -- Choose Your Scenario"):
        st.markdown("""
        Now you need to add your existing money to the system. Choose the scenario that fits you:
        """)
        
        st.markdown("#### 🎯 Scenario 1: You Already Use a Bucket System")
        st.markdown("""
        If you already organize your money by purpose and know exactly how much you have for each bucket (considering you already configured your buckets accordingly):
        
        1. Go to **"Transaction Management"** page
        2. For each bucket, create a transaction:
            - Add a description like "Initial balance for [bucket name]"
            - Select a **positive category** (e.g. +Salary, or create a new one, +Initial Balance)
            - Choose the **location** where this money is stored
            - Select the **specific bucket** (don't use Split Income)
            - Enter the amount you have for that specific bucket
        3. Repeat for all your buckets
        
        **Example**: If you have 1000 in ING and you know 600 is for Necessities and 400 for Fun, create two transactions: one for 600 lei to Necessities bucket and one for 400 lei to Fun bucket, but both with the same location (ING).
        """)
        
        st.markdown("#### 🔄 Scenario 2: You Want to Start Using Buckets")
        st.markdown("""
        If you currently don't use a bucket system and just have money in different accounts and want the app to help you organize it into buckets:
        
        1. Make sure your bucket allocation percentages total 100% (from Step 1)
        2. Go to **"Transaction Management"** page
        3. For each location (account), create a transaction:
            - Add a description like "Initial balance from [location name]"
            - Select a **positive category** (e.g. +Salary, or create a new one, +Initial Balance)
            - Enter the **total amount** you have in that location
            - Choose the **location** where this money is stored
            - **Check "Split Income"** -- this will automatically distribute the money across your buckets according to your allocation percentages
        4. Repeat for all your locations
        
        **Example**: If you have 1000 lei in ING and your buckets are set to Necessities (50%), Economies (30%), Fun (20%), the system will automatically create transactions of 500, 300, and 200 lei to the respective buckets.
        """)
    
    with st.expander("Step 3: Verify Your Setup"):
        st.markdown("""
        After adding your initial money:
        
        1. Go to **"Money Distribution"** page
        2. Check that:
            - Your **total balance** matches your actual money
            - Each **location balance** matches your real accounts
            - **Bucket distribution** looks correct
        3. If something doesn't match, you can edit, add or delete:
            - transactions from "Transaction Management" page, and
            - locations, buckets and categories from "Budget Configuration" page 
        """)
    
    with st.expander("✅ Setup Complete!"):
        st.markdown("""
        Once you've followed these steps, your budget app is fully configured and ready to help you manage your finances effectively!
        If you need help understading how to add transactions properly, see the next section.""")
    
    with st.expander("""💡 Pro Tips for Initial Setup"""):
        st.markdown("""
        - **Take your time** with Step 1 -- good configuration makes everything easier later
        - **Double-check your allocation percentages** add up to 100% before proceeding
        - **Start simple** -- you can always add more categories and buckets later
        - **Verify everything** in Step 3 before starting daily use
        """)
    
    st.success("### 📝 How to add transactions")
    
    with st.expander("🟢 How to record income (positive transactions)", expanded=False):
        st.markdown("""
        0. Make sure you have a positive category created before
        1. Go to "Transaction Management" page
        2. In the "Add transaction" form select a **Positive category** (Salary, Gift, etc.)
        3. Complete the rest of the fields (description, date, amount, location)
        4. You want to split income into buckets?
            - If YES: Check "Split income" to distribute across buckets according to allocation percentages. It doesn't matter the bucket selected. 
            - If NO: Leave "Split income" unchecked but select a specific bucket. The transaction will go directly to that bucket.
        5. Save the transaction
        
        **Note**: If you want to use "Split income" feature, first make sure your bucket allocation is completed (100%). You can check this in "Budget Configuration" page.
        """)
    
    with st.expander("🔴 How to record expenses (negative transactions)", expanded=False):
        st.markdown("""
        0. Make sure you have a negative category created before
        1. Go to "Transaction Management" page
        2. In the "Add transaction" form select a **Negative category** (Bills, Food, Car, etc.)
        3. Enter the amount as a positive number (the system will handle the negative sign)
        4. Complete the rest of the fields (description, date, location, bucket)
        5. Save the transaction
        
        **Note**: "Split income" feature is not available for expenses.
        """)
    
    with st.expander("⚪ How to make neutral transactions (transfers, loans, temporary)", expanded=False):
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
        
        ### Loans / Temporary Transactions
        Create a special neutral category for these kind of transactions.
        ##### If you lend money to someone
        Enter **NEGATIVE AMOUNT** on outgoing transaction (when you give it) and **POSITIVE AMOUNT** on incoming transaction (when you receive them back).
        ##### If you borrow money from someone
        Enter **POSITIVE AMOUNT** on outgoing transaction (when you take it) and **NEGATIVE AMOUNT** on incoming transaction (when you pay them back).
        """)
    
    st.info("### 📊 Understanding Reports")
    
    with st.expander("💰 Money Distribution", expanded=False):
        st.markdown("""
        **Money Distribution** shows your current financial status across all locations and buckets.
        
        **What you'll see:**
        - **Locations chart**: Shows how much money you have in each physical or virtual location
        - **Buckets chart**: Shows how your money is distributed by purpose -- how much money you have available for each purpose
        
        **How to use it:**
        - Check if your actual account balances match what's shown in the locations chart
        - See if your money distribution aligns with your financial goals
        - Identify if any bucket is underfunded or overfunded relative to your needs
        
        💡 **Tip**: This is your financial snapshot -- use it to make decisions about where to allocate more funds or where you might need to cut back.
        
        **Helpful insights:**
        - Try to keep enough money in your "Emergency" bucket to cover 3-6 months of basic expenses
        - If you see too much money sitting in your checking account, consider moving some to savings or other buckets
        - Check this report before making big purchases to see if you really have the money available
        - Use this report to have honest family conversations about where your money is and where it should be
        """)
    
    with st.expander("📅 Monthly Report", expanded=False):
        st.markdown("""
        **Monthly Report** breaks down your transactions by category for a specific month.
        
        **What you'll see:**
        - **Positive categories**: Income sources for the selected month
        - **Negative categories**: Expenses for the selected month
        - **Neutral categories**: Transfers and temporary transactions
        
        **How to use it:**
        - Track your monthly income and spending patterns
        - Identify your biggest expense categories
        - Compare your spending against your budget
        - Spot unusual transactions or spending spikes
        
        💡 **Tip**: Use the month selector to compare different months and identify trends or seasonal patterns in your finances.
        
        **Helpful insights:**
        - A simple rule of thumb: Try to save at least 10-15% of your monthly income
        - Look for your "money leaks" -- small, frequent expenses that add up (like daily coffee or subscriptions)
        - If groceries, eating out, or entertainment seem high, try tracking these more closely for a month
        - Notice which weeks of the month you spend the most and plan accordingly
        - Compare your utility bills month-to-month to spot seasonal changes or potential problems
        - Celebrate months where you spent less than planned and try to understand what worked well
        """)
    
    with st.expander("🗓️ Yearly Report", expanded=False):
        st.markdown("""
        **Yearly Report** provides a month-by-month breakdown of your finances for a specific year.
        
        **What you'll see:**
        - **Category breakdown**: Total amounts for each category for the year
        - **Monthly progression**: How your income, expenses, and balance changed throughout the year
        - **Category tables**: Detailed breakdown of each category by month
        
        **How to use it:**
        - Identify seasonal patterns in your income or spending
        - Track your financial progress throughout the year
        - See which months had unusual financial activity
        - Plan for recurring annual expenses
        
        💡 **Tip**: Look for months with significant financial changes and analyze what caused them to better prepare for similar situations in the future.
        
        **Helpful insights:**
        - Use this report to plan for predictable yearly expenses like holidays, back-to-school, or vacations
        - Notice which months are typically tight and which have extra money -- this helps with yearly planning
        - Look at how much you spent in total on "wants" vs "needs" -- is the balance right for your family?
        - Did you save as much as you hoped this year? If not, what months threw you off track?
        - Use this report when setting goals for next year -- make them realistic based on your actual patterns
        - Consider setting a "spending cap" for categories that consistently went over budget
        """)
    
    with st.expander("📊 Historical Report", expanded=False):
        st.markdown("""
        **Historical Report** shows your financial trends across multiple years.
        
        **What you'll see:**
        - **Year-by-year comparison**: How your finances have evolved over time
        - **Category trends**: How spending in different categories has changed over years
        - **Long-term balance**: Your overall financial growth or decline
        
        **How to use it:**
        - Evaluate your long-term financial progress
        - Identify multi-year trends in your income and spending
        - Track how your financial habits have changed over time
        - Set realistic long-term financial goals based on historical data
        
        💡 **Tip**: This report is especially valuable for identifying slow changes in your financial habits that might not be obvious in shorter timeframes.
        
        **Helpful insights:**
        - Are you saving more each year than the year before? Even small increases add up over time
        - Watch for "expense creep" -- categories that grow a little each year can eventually strain your budget
        - Has your family's spending changed as your life changed (new baby, new house, etc.)?
        - Look at how much your total savings have grown over the years -- seeing progress is motivating!
        - Use this report to have family discussions about long-term goals like education funds or retirement
        - If your expenses in a category have decreased over time, celebrate that win and learn from it
        - Notice if your income is growing faster than your expenses -- that's a great sign for financial health
        """)

    st.info("""
    ### 💡 Tips & Best Practices
    - **If this is your first time using the app**, we recommend you to go through the "Initial Setup" section first.
    - **Regularly review** your transactions to ensure accuracy
    - **Use consistent categories** to make your reports more meaningful
    - **Use Split Income** for regular income like salary to automatically distribute across buckets
    - **Check your balances** periodically to ensure they match your actual accounts
    - **Use descriptive transaction names** to help you remember what each transaction was for
    """)

    st.warning("""
    ### ⚠️ Important Warning
    **All changes made in this system are permanent.** Please be careful when adding, editing, or deleting data. 
    There is no automatic "undo" feature, so double-check your entries before confirming them.
    """)
    
    st.success("""
    ### 🎉 That's it!
    🤩 With these guidelines, you should be able to use the app efficiently and manage your finances with ease! Enjoy!
    """)

    st.error("""
    ### ❗️ Bugs & Errors
    If you encounter any bugs or errors, please email us at contact@elisei.pro with as many details as possible — ideally including screenshots. We'll get back to you with a solution as soon as we can. Thank you!
    """)
