import streamlit as st
from functions import brands, get_all_export_from_brand, get_data_from_table, get_rows_with_selected, translate_rows, sidebar


st.set_page_config(page_title="TrustpilotExtract - Reviews", page_icon="✨", layout="wide")

with st.sidebar:
    sidebar()

st.title("Get brand reviews")

list_brands = brands()

selected_brand = st.selectbox(
    label="Select brand",
    options=list_brands
)

if selected_brand != "":
    list_exports = get_all_export_from_brand(selected_brand)
    if len(list_exports) == 0:
        st.write("No reviews found for this brand")
    else:
        selected_export = st.selectbox(
            label="Select export",
            options=list_exports
        )
        if selected_export != "":
            data = get_data_from_table(selected_export)
            column_config = {

                    "select": st.column_config.CheckboxColumn(
                        "Select", help="Edit review", width='small', disabled=False
                    ),
                    "name": st.column_config.TextColumn(
                        "Author", help="Author of review", max_chars=100,width='medium', disabled=True
                    ),
                    "rating": st.column_config.TextColumn(
                        label="Rating",
                        help="Rating of review",
                        width='small',
                        disabled=True
                    ),
                    "title": st.column_config.TextColumn(
                        "Title", help="Title of review", max_chars=100, disabled=True
                    ),
                    "review": st.column_config.TextColumn(
                        "Content", help="Content of review", max_chars=100, disabled=True
                    ),
                    "locale": st.column_config.TextColumn(
                        "Locale", help="Locale of review", max_chars=100, disabled=True
                    ),
                    "published_date": st.column_config.DatetimeColumn(
                        "Published date", help="Published date of review",
                        format="D MMM YYYY, h:mm a", width='medium', disabled=True
                    ),



            }
            actual_data = st.data_editor(
                data,
                column_config=column_config,
                use_container_width=True,
                hide_index=True
            )

            rows_selected = get_rows_with_selected(actual_data)

            if len(rows_selected) > 0:
                if st.button(label="Translate selected reviews"):
                    try :
                        updated_date = translate_rows(rows_selected, selected_export)
                        st.write(updated_date)
                    except Exception as e:
                        st.error(e)
                        pass
