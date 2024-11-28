import streamlit as st
import joblib
import pandas as pd

# Load the saved model (pipeline)
pipeline = joblib.load('best_model.joblib')


# Custom CSS to center the title
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Title for the app
st.markdown('<div class="title">House Price Prediction</div>', unsafe_allow_html=True)

# Display the image after the title using the new 'use_container_width' parameter
st.image('houses.png', use_container_width=True)  # Adjust path as needed

# Create two columns for sliders and the select slider
col1, col2 = st.columns(2)

# Column 1: Numeric sliders for 'area', 'bedrooms', 'bathrooms'
with col1:
    user_input = {
        'area': st.slider("Enter area (in square feet)", min_value=1000, max_value=1800, value=1200),
        'bedrooms': st.slider("Number of bedrooms", min_value=1, max_value=10, value=3),
        'bathrooms': st.slider("Number of bathrooms", min_value=1, max_value=5, value=2)
    }

# Column 2: Numeric sliders for 'stories', 'parking', and 'furnishing status'
with col2:
    user_input.update({
        'stories': st.slider("Number of stories", min_value=1, max_value=5, value=1),
        'parking': st.slider("Parking spaces", min_value=0, max_value=5, value=1),
        'furnishingstatus': st.select_slider(
            label="Furnishing status",
            options=["furnished", "semi-furnished", "unfurnished"],
            value="semi-furnished",  # Default is "semi-furnished"
            label_visibility="visible",
            key="furnishingstatus_slider"
        )
    })




# Create three columns for segmented controls (yes/no questions)
col1, col2, col3 = st.columns(3)

# Segment control for binary questions (YES/NO) in three columns
with col1:
    user_input['mainroad'] = st.segmented_control(
        label="Is it near the main road?",
        options=["YES", "NO"],
        default="NO",  # Default is "NO"
        label_visibility="visible",
        key="mainroad_segmented"
    )

    user_input['hotwaterheating'] = st.segmented_control(
        label="Does it have hot water heating?",
        options=["YES", "NO"],
        default="NO",  # Default is "NO"
        label_visibility="visible",
        key="hotwaterheating_segmented"
    )

with col2:
    user_input['basement'] = st.segmented_control(
        label="Does it have a basement?",
        options=["YES", "NO"],
        default="NO",  # Default is "NO"
        label_visibility="visible",
        key="basement_segmented"
    )

    user_input['airconditioning'] = st.segmented_control(
        label="Does it have air conditioning?",
        options=["YES", "NO"],
        default="NO",  # Default is "NO"
        label_visibility="visible",
        key="airconditioning_segmented"
    )

with col3:
    user_input['guestroom'] = st.segmented_control(
        label="Does it have a guest room?",
        options=["YES", "NO"],
        default="NO",  # Default is "NO"
        label_visibility="visible",
        key="guestroom_segmented"
    )

    user_input['prefarea'] = st.segmented_control(
        label="Is it in a preferred area?",
        options=["YES", "NO"],
        default="NO",  # Default is "NO"
        label_visibility="visible",
        key="prefarea_segmented"
    )



# Safely handle the user inputs to ensure they are not None
def safe_lower(value):
    if value:
        return value.lower()
    return "no"  # Default to "no" if the value is None or empty

# Convert "YES" / "NO" inputs to lowercase for the model
user_input['mainroad'] = safe_lower(user_input['mainroad'])
user_input['hotwaterheating'] = safe_lower(user_input['hotwaterheating'])
user_input['basement'] = safe_lower(user_input['basement'])
user_input['airconditioning'] = safe_lower(user_input['airconditioning'])
user_input['guestroom'] = safe_lower(user_input['guestroom'])
user_input['prefarea'] = safe_lower(user_input['prefarea'])


# Add custom CSS for styling
st.markdown("""
    <style>
    .centered-result {
        text-align: center;
        background-color: #d4edda; /* Light green background */
        color: #155724; /* Dark green text */
        padding: 20px;
        border-radius: 10px;
        font-size: 24px; /* Bigger font size */
        font-weight: bold; /* Bold text */
        margin-top: 20px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Display the result in the center after clicking "Predict"
if st.button("Predict"):
    # Convert user input to a DataFrame
    input_df = pd.DataFrame([user_input])
    
    # Use the pipeline directly for prediction
    prediction = pipeline.predict(input_df)
    
    # Display the result in the center with updated styling
    st.markdown(f"""
        <div class="centered-result">
            Estimated House Price: ${prediction[0]:,.0f}
        </div>
    """, unsafe_allow_html=True)
