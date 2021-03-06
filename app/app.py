import datetime
import os

import constants
import streamlit as st
import utils
from google.cloud import storage


def main(img_location, error_location, storage_client):

    pwd = st.session_state.get("password")
    if not pwd:
        pwd = st.sidebar.text_input("Password:", value="", type="password")

    if pwd == constants.CLASSIFICATION_PASSWORD:
        st.session_state["password"] = pwd

        spot_names = utils.get_spot_names()
        spot_names.sort()
        
        st.sidebar.image(str(constants.LOGO_PATH), use_column_width=True)

        # Take selected spot and parse name and timezone
        classification_type = st.sidebar.selectbox(
            "Please select a classification type.", ["Gating", "Surf Quality"]
        )
        selected_spot = st.sidebar.selectbox(
            "Please select a spot.", spot_names, index=0
        )

        startdate = st.sidebar.date_input(
            "Start Date", (datetime.date.today() - datetime.timedelta(days=1))
        )
        enddate = st.sidebar.date_input("End Date", datetime.date.today())

        start_time = st.sidebar.time_input("Start Time", datetime.time(6))
        end_time = st.sidebar.time_input("End Time", datetime.time(18))

        time_range = (start_time.hour, end_time.hour)
        
        
        link = '[Frame Summary](https://labeling.summary.surfline.ai)'
        st.markdown(link, unsafe_allow_html=True)

        if classification_type == "Surf Quality":
            # Write first frame to the page
            utils.get_frame(
                classification="quality",
                spot_prefix=selected_spot,
                start_date=startdate,
                end_date=enddate,
                time_range=time_range,
                img_location=img_location,
                error_location=error_location
            )
            cols = st.columns(2)
            with cols[0]:
                if st.button("Skip Frame"):
                    utils.skip_frame(classification="quality")
                    utils.get_frame(
                        classification="quality",
                        spot_prefix=selected_spot,
                        start_date=startdate,
                        end_date=enddate,
                        time_range=time_range,
                        img_location=img_location,
                        error_location=error_location
                    )
            with cols[1]:
                if st.button("Undo Last Classification"):
                    utils.undo_previous_classification(
                        image_location=img_location,
                        storage_client=storage_client
                        )
                    utils.get_frame(
                        classification="quality",
                        spot_prefix=selected_spot,
                        start_date=startdate,
                        end_date=enddate,
                        time_range=time_range,
                        img_location=img_location,
                        error_location=error_location
                )

            cols = st.columns(3)
            # Classify frame as poor conditions
            with cols[0]:
                if st.button("Poor"):
                    frame_name = st.session_state["cur_frame_name"]
                    frame_path = os.path.join(constants.POOR_PREFIX, frame_name)
                    utils.save_frame(frame_path, storage_client)
                    utils.get_frame(
                        classification="quality",
                        spot_prefix=selected_spot,
                        start_date=startdate,
                        end_date=enddate,
                        time_range=time_range,
                        img_location=img_location,
                        error_location=error_location
                    )

            # Classify frame as fair conditions
            with cols[1]:
                if st.button("Fair"):
                    frame_name = st.session_state["cur_frame_name"]
                    frame_path = os.path.join(constants.FAIR_PREFIX, frame_name)
                    utils.save_frame(frame_path, storage_client)
                    utils.get_frame(
                        classification="quality",
                        spot_prefix=selected_spot,
                        start_date=startdate,
                        end_date=enddate,
                        time_range=time_range,
                        img_location=img_location,
                        error_location=error_location
                    )

            # Classify frame as good conditions
            with cols[2]:
                if st.button("Good"):
                    frame_name = st.session_state["cur_frame_name"]
                    frame_path = os.path.join(constants.GOOD_PREFIX, frame_name)
                    utils.save_frame(frame_path, storage_client)
                    utils.get_frame(
                        classification="quality",
                        spot_prefix=selected_spot,
                        start_date=startdate,
                        end_date=enddate,
                        time_range=time_range,
                        img_location=img_location,
                        error_location=error_location
                    )

        if classification_type == "Gating":
            # Write initial frame to page
            utils.get_frame(
                classification="gating",
                spot_prefix=selected_spot,
                start_date=startdate,
                end_date=enddate,
                time_range=time_range,
                img_location=img_location,
                error_location=error_location
            )
            cols = st.columns(2)
            with cols[0]:
                if st.button("Skip Frame"):
                    utils.skip_frame(classification="gating")
                    utils.get_frame(
                        classification="gating",
                        spot_prefix=selected_spot,
                        start_date=startdate,
                        end_date=enddate,
                        time_range=time_range,
                        img_location=img_location,
                        error_location=error_location
                    )
            with cols[1]:
                if st.button("Undo Last Classification"):
                    utils.undo_previous_classification(
                        image_location=img_location,
                        storage_client=storage_client
                        )
                    utils.get_frame(
                        classification="quality",
                        spot_prefix=selected_spot,
                        start_date=startdate,
                        end_date=enddate,
                        time_range=time_range,
                        img_location=img_location,
                        error_location=error_location
                    )

            cols = st.columns(2)
            # Classify frame as inactive for gating
            with cols[0]:
                if st.button("Visible"):
                    frame_name = st.session_state["cur_frame_name"]
                    frame_path = os.path.join(constants.ACTIVE_PREFIX, frame_name)
                    utils.save_frame(frame_path, storage_client)
                    utils.get_frame(
                        classification="gating",
                        spot_prefix=selected_spot,
                        start_date=startdate,
                        end_date=enddate,
                        time_range=time_range,
                        img_location=img_location,
                        error_location=error_location
                    )

            # Classify frame as inactive for gating
            with cols[1]:
                if st.button("Not Visible"):
                    frame_name = st.session_state["cur_frame_name"]
                    frame_path = os.path.join(constants.INACTIVE_PREFIX, frame_name)
                    utils.save_frame(frame_path, storage_client)
                    utils.get_frame(
                        classification="gating",
                        spot_prefix=selected_spot,
                        start_date=startdate,
                        end_date=enddate,
                        time_range=time_range,
                        img_location=img_location,
                        error_location=error_location
                        
                    )


if __name__ == "__main__":
    st.set_page_config(layout="wide")

    storage_client = storage.Client()
    img_location = st.empty()
    error_location = st.empty()
    main(img_location, error_location, storage_client)
