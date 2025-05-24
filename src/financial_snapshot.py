import streamlit as st

def show_financial_snapshot():
    st.title("🏖️ Retirement Lifestyle Planner")
    st.header("Financial Snapshot")

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
