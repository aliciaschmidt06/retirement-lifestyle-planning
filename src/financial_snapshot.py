import streamlit as st

def calculate_canadian_tax(gross_salary):
    """Calculate approximate Canadian federal + provincial tax (Ontario rates as example)"""
    if gross_salary <= 0:
        return 0
    
    # Simplified 2026 Canadian tax brackets (federal + Ontario)
    # These are approximate combined marginal rates
    tax = 0
    if gross_salary > 235_675:
        tax += (gross_salary - 235_675) * 0.5353
        gross_salary = 235_675
    if gross_salary > 173_205:
        tax += (gross_salary - 173_205) * 0.5353
        gross_salary = 173_205
    if gross_salary > 165_430:
        tax += (gross_salary - 165_430) * 0.5153
        gross_salary = 165_430
    if gross_salary > 106_717:
        tax += (gross_salary - 106_717) * 0.4341
        gross_salary = 106_717
    if gross_salary > 102_894:
        tax += (gross_salary - 102_894) * 0.4341
        gross_salary = 102_894
    if gross_salary > 55_867:
        tax += (gross_salary - 55_867) * 0.2965
        gross_salary = 55_867
    if gross_salary > 53_359:
        tax += (gross_salary - 53_359) * 0.2915
        gross_salary = 53_359
    if gross_salary > 49_231:
        tax += (gross_salary - 49_231) * 0.2415
        gross_salary = 49_231
    # Base bracket
    tax += gross_salary * 0.2005
    
    return tax

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
    takehome_salaries = []
    with col5:
        salary = st.number_input("Gross Yearly Salary ($)", min_value=0.0, value=0.0, step=25000.0)
        salaries.append(salary)
        if salary > 0:
            tax = calculate_canadian_tax(salary)
            takehome = salary - tax
            takehome_salaries.append(takehome)
            st.caption(f"💵 Estimated take-home: ${takehome:,.2f} (after ~${tax:,.2f} tax)")
    with col6:
        add_salary = st.checkbox("Add another salary")
        if add_salary:
            salary2 = st.number_input("Additional Gross Yearly Salary ($)", min_value=0.0, value=0.0, step=25000.0)
            salaries.append(salary2)
            if salary2 > 0:
                tax2 = calculate_canadian_tax(salary2)
                takehome2 = salary2 - tax2
                takehome_salaries.append(takehome2)
                st.caption(f"💵 Estimated take-home: ${takehome2:,.2f} (after ~${tax2:,.2f} tax)")

    col7, col8 = st.columns(2)
    with col7:
        debt = st.number_input("Total Debt ($)", min_value=0.0, value=0.0, step=5000.0)
    with col8:
        investments = st.number_input("Current Investment Holdings ($)", min_value=0.0, value=0.0, step=10000.0)

    total_salary = sum(salaries)
    total_takehome = sum(takehome_salaries)

    st.markdown("---")
    st.subheader("💰 Summary")
    st.write(f"**Total Household Gross Salary:** ${total_salary:,.2f}")
    if total_takehome > 0:
        st.write(f"**Total Household Take-Home:** ${total_takehome:,.2f}")
    net_worth = (assets + investments) - debt
    st.write(f"**Net Worth (Assets - Debt + Investments):** ${net_worth:,.2f}")
