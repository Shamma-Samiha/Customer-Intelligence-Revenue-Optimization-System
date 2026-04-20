import streamlit as st


def show_table(df, title: str):
    st.markdown(
        f'''
        <div class="table-shell">
            <div class="table-title">{title}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )
    st.dataframe(df, use_container_width=True, hide_index=True, height=380)
