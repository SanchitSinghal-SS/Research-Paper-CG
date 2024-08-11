import streamlit as st

# Page Navigation


def main():
    st.set_page_config(
        page_title="Company Performance Dashboard", layout="wide")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a Page", ["Company Details", "Industry Performance"])

    if page == "Company Details":
        import pages.company_details as page1
        page1.show()
    elif page == "Industry Performance":
        import pages.industry_performance as page2
        page2.run_page_2()


if __name__ == "__main__":
    main()
