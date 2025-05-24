import streamlit as st
import os
import json
import matplotlib.pyplot as plt

def show_retirement_planner():
    st.title("\U0001F3D6️ Retirement Lifestyle Planner")
    st.header("Retirement Projection Calculator")

    SCENARIOS_DIR = "scenarios"
    os.makedirs(SCENARIOS_DIR, exist_ok=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        capital = st.number_input("Current Capital ($)", min_value=0.0, value=0.0, step=1000.0)
    with col2:
        age = st.number_input("Your Current Age", min_value=0, max_value=100, value=30)
    with col3:
        interest = st.number_input("Expected Annual Interest Rate (%)", min_value=0.0, value=7.0, step=0.1)

    if "contribution_rows" not in st.session_state:
        st.session_state.contribution_rows = 1
    if "contributions" not in st.session_state:
        st.session_state.contributions = []

    st.subheader("Contribution Phases")
    new_contributions = []
    for i in range(st.session_state.contribution_rows):
        col1, col2 = st.columns(2)
        with col1:
            contrib = st.number_input(f"Annual Contribution #{i+1}", min_value=0.0, step=1000.0, key=f"contrib_{i}")
        with col2:
            yrs = st.number_input(f"Years #{i+1}", min_value=1, max_value=100, step=1, key=f"years_{i}")
        new_contributions.append((contrib, yrs))

    if st.button("➕ Add Another Contribution Phase"):
        st.session_state.contribution_rows += 1
        st.rerun()

    if st.button("📈 Calculate Retirement Funds"):
        r = interest / 100
        total_years = 0
        total_value = capital

        for c, y in new_contributions:
            total_value = total_value * (1 + r) ** y + c * (((1 + r) ** y - 1) / r)
            total_years += y

        retirement_age = age + total_years
        st.session_state.future_value = total_value
        st.session_state.retirement_age = retirement_age
        st.session_state.age = age
        st.success(f"You'll have **${total_value:,.2f}** by age **{retirement_age}**.")

    if "future_value" in st.session_state:
        with st.expander("💾 Save this Scenario for Comparison"):
            with st.form("save_scenario_form"):
                scenario_name = st.text_input("Scenario Name")
                save_clicked = st.form_submit_button("💾 Save Scenario")
                if save_clicked:
                    if scenario_name.strip() == "":
                        st.warning("Please enter a scenario name.")
                    else:
                        scenario_data = {
                            "name": scenario_name,
                            "capital": capital,
                            "age": age,
                            "interest": interest,
                            "contributions": new_contributions,
                            "future_value": st.session_state.future_value,
                            "retirement_age": st.session_state.retirement_age,
                        }
                        try:
                            with open(os.path.join(SCENARIOS_DIR, f"{scenario_name}.json"), "w") as f:
                                json.dump(scenario_data, f, indent=2)
                            st.success(f"Scenario '{scenario_name}' saved successfully.")
                        except Exception as e:
                            st.error(f"Failed to save scenario: {e}")

    st.header("Post-Retirement Spending Plan")

    if "future_value" in st.session_state and "retirement_age" in st.session_state:
        col12, col13 = st.columns(2)
        with col12:
            target = st.number_input(
                "Target death age (lol)",
                min_value=st.session_state.age + 1,
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
                st.info(f"or **${monthly_spending:,.2f}**/month until age {target} (years to spend: {remaining_years})")
        else:
            st.warning("You will be 100 or older at the end of your investment period.")
    else:
        st.info("\U0001F446 Calculate retirement funds first to unlock this section.")

    st.sidebar.header("📊 Compare Retirement Scenarios")
    scenario_files = [f for f in os.listdir(SCENARIOS_DIR) if f.endswith(".json")]
    selected_files = st.sidebar.multiselect("Select Scenarios to Compare", scenario_files)

    if st.sidebar.button("Compare Selected Scenarios") and selected_files:
        fig, ax = plt.subplots()

        for file in selected_files:
            with open(os.path.join(SCENARIOS_DIR, file)) as f:
                data = json.load(f)
                initial_age = data["age"]
                initial_value = data["capital"]
                r = data["interest"] / 100
                x_vals = []
                y_vals = []

                age = initial_age
                value = initial_value

                for contrib, yrs in data["contributions"]:
                    for _ in range(yrs):
                        value = value * (1 + r) + contrib
                        x_vals.append(age)
                        y_vals.append(value)
                        age += 1

                ax.plot(x_vals, y_vals, label=f"{data['name']} ({data['interest']}%)")

        ax.set_xlabel("Age")
        ax.set_ylabel("Investment Value ($)")
        ax.set_title("Retirement Scenario Comparison")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
