import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="MedAI-Nexus",
    page_icon="🩺",
    layout="wide",
)


st.title("🩺 MedAI-Nexus")
st.subheader("AI-Powered Medical Report Analyzer")

st.write(
    "Upload a blood report PDF to extract and analyze "
    "common blood-test parameters."
)

st.info(
    "Research prototype only. This application does not provide "
    "medical diagnosis or treatment advice."
)


uploaded_file = st.file_uploader(
    "📄 Upload Blood Report",
    type=["pdf"],
)


if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("🔍 Analyze Report"):

        with st.spinner("Analyzing blood report..."):

            try:
                response = requests.post(
                    f"{API_URL}/analyze/blood-report",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf",
                        )
                    },
                    timeout=60,
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "✅ Blood report analyzed successfully."
                    )

                    # -----------------------------
                    # Extracted Values
                    # -----------------------------

                    st.subheader("📋 Extracted Values")

                    st.json(result["extracted_values"])

                    # -----------------------------
                    # Blood Test Analysis
                    # -----------------------------

                    st.subheader("🧪 Blood Test Analysis")

                    analysis_results = result["analysis"]

                    test_names = list(analysis_results.keys())

                    for start in range(0, len(test_names), 2):

                        columns = st.columns(2)

                        for index, test_name in enumerate(
                            test_names[start:start + 2]
                        ):

                            analysis = analysis_results[test_name]

                            value = analysis.get(
                                "value",
                                "N/A"
                            )

                            unit = analysis.get(
                                "unit",
                                ""
                            )

                            reference_range = analysis.get(
                                "reference_range",
                                []
                            )

                            status = analysis.get(
                                "status",
                                "unknown"
                            )

                            with columns[index]:

                                st.markdown(
                                    f"### {test_name.title()}"
                                )

                                st.metric(
                                    label="Reported Value",
                                    value=f"{value} {unit}",
                                )

                                if len(reference_range) == 2:

                                    st.caption(
                                        f"Reference range: "
                                        f"{reference_range[0]} – "
                                        f"{reference_range[1]} "
                                        f"{unit}"
                                    )

                                if status == (
                                    "within_reference_range"
                                ):

                                    st.success(
                                        "✅ Within reference range"
                                    )

                                elif status == (
                                    "above_reference_range"
                                ):

                                    st.warning(
                                        "⚠️ Above reference range"
                                    )

                                elif status == (
                                    "below_reference_range"
                                ):

                                    st.warning(
                                        "⚠️ Below reference range"
                                    )

                                else:

                                    st.info(
                                        f"ℹ️ {status}"
                                    )

                                st.divider()

                    # -----------------------------
                    # Disclaimer
                    # -----------------------------

                    st.caption(
                        result["disclaimer"]
                    )

                else:

                    st.error(
                        f"API returned an error: "
                        f"{response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to the "
                    "MedAI-Nexus API. "
                    "Make sure FastAPI is running "
                    "on port 8000."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "⏱️ The analysis request timed out. "
                    "Please try again."
                )

            except Exception as error:

                st.error(
                    f"❌ Unexpected error: {error}"
                )