import streamlit as st


def show_table(df, title: str):
    csv = df.to_csv(index=False).encode("utf-8")
    st.markdown(
        f'''
        <div class="table-shell">
            <div class="table-title">{title}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )
    st.download_button(
        "Download CSV",
        csv,
        file_name=f"{title.lower().replace(' ', '_')}.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.dataframe(df, use_container_width=True, hide_index=True, height=380)
