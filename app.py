import streamlit as st

st.set_page_config(page_title="Retirement Lifestyle Planner", layout="wide")
st.title("🏖️ Retirement Lifestyle Planner")

# ---- Section 1: Financial Snapshot ----
st.header("1. Financial Snapshot")

col1, col2, col3, col4 = st.columns(4)
with col1:
    car = st.number_input("Car value ($)", min_value=0.0, value=0.0, step=5000.0)
with col2:
    house = st.number_input("House value ($)", min_value=0.0, value=0.0, step=5000.0)
with col3:
    other = st.number_input("Other assets? ($)", min_value=0.0, value=0.0, step=5000.0)
with col4:
    savings = st.number_input("Savings ($)", min_value=0.0, value=0.0, step=5000.0)

assets = car + house + savings + other

col5, col6 = st.columns(2)
salaries = []
with col5:
    salary = st.number_input("Yearly Salary ($)", min_value=0.0, value=0.0, step=25000.0)
    salaries.append(salary)
with col6:
    add_salary = st.checkbox("Add another salary")
    if add_salary:
        salary2 = st.number_input("Additional Yearly Salary ($)", min_value=0.0, value=0.0, step=25000.0)
        salaries.append(salary2)

col7, col8 = st.columns(2)
with col7:
    debt = st.number_input("Total Debt ($)", min_value=0.0, value=0.0, step=5000.0)
with col8:
    investments = st.number_input("Current Investment Holdings ($)", min_value=0.0, value=0.0, step=10000.0)

total_salary = sum(salaries)

st.markdown("---")
st.subheader("💰 Summary")
st.write(f"**Total Household Salary:** ${total_salary:,.2f}")
net_worth = (assets + investments) - debt
st.write(f"**Net Worth (Assets - Debt + Investments):** ${net_worth:,.2f}")

# ---- Section 2: Retirement Calculator ----
st.header("2. Retirement Projection Calculator")

col9, col10, col11 = st.columns(3)
with col9:
    capital = st.number_input("Current Capital ($)", min_value=0.0, value=0.0, step=25000.0)
    contribution = st.number_input("Annual Contribution ($)", min_value=0.0, value=0.0, step=1000.0)
with col10:
    age = st.number_input("Your Current Age", min_value=0, max_value=100, value=30)
    years = st.number_input("Number of Years to Contribute", min_value=0, max_value=70, value=30)
with col11:
    interest = st.number_input("Expected Annual Interest Rate (%)", min_value=0.0, value=5.0, step=1.0)

if st.button("📈 Calculate Retirement Funds"):
    r = interest / 100
    future_value = capital * (1 + r) ** years + contribution * (((1 + r) ** years - 1) / r)
    retirement_age = age + years
    st.session_state.future_value = future_value
    st.session_state.retirement_age = retirement_age
    st.session_state.age = age  # needed for validation later
    st.success(f"You'll have ${future_value:,.2f} by age {retirement_age}.")

# ---- Section 3: Post-Retirement Spending Plan ----
st.header("3. Post-Retirement Spending Plan")

if "future_value" in st.session_state and "retirement_age" in st.session_state:
    col12, col13 = st.columns(2)
    with col12:
        target = st.number_input(
            "Target death age (lol)",
            min_value=st.session_state.age,
            max_value=130,
            value=100,
            key="target_age"
        )

    remaining_years = target - st.session_state.retirement_age
    if remaining_years > 0:
        yearly_spending = st.session_state.future_value / remaining_years
        monthly_spending = yearly_spending / 12
        with col13:
            st.info(f"Spend about **${yearly_spending:,.2f}**/year")
            st.info(f"or **${monthly_spending:,.2f}**/month until age {target} (years to spend it: {remaining_years})")
    else:
        st.warning("You will be 100 or older at the end of your investment period.")
else:
    st.info("👆 Calculate retirement funds first to unlock this section.")
