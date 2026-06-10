from io import BytesIO

import cv2
import easyocr
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="Photo To Excel",
    layout="wide",
)

st.title("📷 Photo To Excel")

st.markdown(
    """
### Photo Rules

- Landscape mode
- Maximum 10 rows per photo
- Include column headers
- No blur
- No glare
- Fill most of the frame with the table
"""
)


@st.cache_resource
def load_reader():
    return easyocr.Reader(["en"], gpu=False)


def calculate_blur_score(image: np.ndarray) -> float:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def image_quality_check(image: np.ndarray):
    height, width = image.shape[:2]

    blur_score = calculate_blur_score(image)

    errors = []

    if width < 1200:
        errors.append(
            f"Low resolution detected ({width}px). Recommended: 1200px+"
        )

    if blur_score < 100:
        errors.append(
            f"Image appears blurry (score={blur_score:.0f})"
        )

    return errors, blur_score


def preprocess(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC,
    )

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    binary = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2,
    )

    return binary


def extract_text(reader, image: np.ndarray):
    results = reader.readtext(
        image,
        detail=1,
        paragraph=False,
    )

    rows = []

    for item in results:
        _, text, confidence = item

        if confidence < 0.30:
            continue

        rows.append(
            {
                "Text": text,
                "Confidence": round(confidence, 3),
            }
        )

    return pd.DataFrame(rows)


uploaded_files = st.file_uploader(
    "Upload Photos",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
)

if uploaded_files:

    reader = load_reader()

    combined_df = pd.DataFrame()

    for uploaded_file in uploaded_files:

        st.divider()
        st.subheader(uploaded_file.name)

        image = Image.open(uploaded_file).convert("RGB")

        image_np = np.array(image)
        image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        st.image(image)

        errors, blur_score = image_quality_check(image_cv)

        st.write(f"Blur Score: {blur_score:.0f}")

        if errors:
            for error in errors:
                st.warning(error)

            st.error(
                "Photo quality is poor. Ask user to retake."
            )

        processed = preprocess(image_cv)

        with st.spinner("Running OCR..."):
            df = extract_text(reader, processed)

        if not df.empty:
            combined_df = pd.concat(
                [combined_df, df],
                ignore_index=True,
            )

    if not combined_df.empty:

        st.divider()
        st.subheader("OCR Results")

        st.dataframe(
            combined_df,
            use_container_width=True,
        )

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl",
        ) as writer:
            combined_df.to_excel(
                writer,
                index=False,
                sheet_name="OCR_Data",
            )

        output.seek(0)

        st.download_button(
            label="📥 Download Excel",
            data=output,
            file_name="photo_to_excel.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.warning("No text detected.")
