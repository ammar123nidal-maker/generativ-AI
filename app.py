import streamlit as st
from openai import OpenAI
import json

# ====== OpenAI Client ======
client = OpenAI(api_key="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")  # ضع مفتاحك هنا

# ====== Build the Prompt ======
def build_prompt(diseases, age, weight, height, activity_level):
    return f"""
    You are a medical and lifestyle assistant.  
    Based on the following patient profile, generate structured personalized advice:

    Patient Information:
    - Disease/Condition: {diseases}
    - Age: {age}
    - Weight: {weight} kg
    - Height: {height} cm
    - Activity Level: {activity_level}

    Provide recommendations in the following categories:

    1. Diet Recommendations – 3–5 personalized and practical suggestions.  
    2. Exercise Recommendations – 3–5 safe and suitable exercises for the given condition and activity level.  
    3. Daily Monitoring Habits – 2–4 key metrics the patient should track daily.  
    4. Stress/Sleep Management – 2–4 strategies tailored to the patient’s profile.  
    5. Red Flags / When to Seek Care – specific warning signs related to the patient’s disease/condition.

    Output the response strictly in structured JSON format like this example:

    {{
      "diet_recommendations": [""],
      "exercise_recommendations": [""],
      "daily_monitoring": [""],
      "stress_sleep_management": [""],
      "red_flags": [""]
    }}

    Ensure the advice is safe, practical, and easy to understand for the patient.
    """

# ====== Generate Advice from AI ======
def get_structured_info(diseases, age, weight, height, activity_level):
    prompt = build_prompt(diseases, age, weight, height, activity_level)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful and safe medical and lifestyle assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

# ====== Streamlit App UI ======
st.set_page_config(page_title="AI Lifestyle Advisor", page_icon="💊", layout="centered")

st.title("💊 AI-Powered Lifestyle & Health Advisor")
st.write("This tool provides personalized health and lifestyle advice using AI (for educational purposes only).")

# --- User Inputs ---
st.header("🧍 Patient Information")

col1, col2 = st.columns(2)
with col1:
    diseases = st.text_input("Medical Condition(s)", placeholder="e.g. Diabetes, Hypertension")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    weight = st.number_input("Weight (kg)", min_value=10.0, step=0.5)
with col2:
    height = st.number_input("Height (cm)", min_value=50.0, step=0.5)
    activity_level = st.selectbox("Activity Level", ["Low", "Moderate", "High"])

# --- Generate Button ---
if st.button("Generate Personalized Advice"):
    with st.spinner("Generating AI recommendations... 💭"):
        result = get_structured_info(diseases, age, weight, height, activity_level)

        st.success("✅ AI Recommendations Generated Successfully!")

        # Try to parse as JSON
        try:
            parsed_result = json.loads(result)
            st.subheader("📋 Personalized Recommendations")
            st.json(parsed_result)
        except:
            st.warning("⚠️ Could not parse as JSON, showing raw output instead:")
            st.write(result)

st.divider()
st.info("⚕️ Disclaimer: This tool is for educational purposes only. Always consult your healthcare provider before making health-related decisions.")
