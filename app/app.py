import streamlit as st
import pandas as pd
import joblib
from pymongo import MongoClient
from sklearn.preprocessing import LabelEncoder

# Load model
model = joblib.load("D:\\NIDS\\model\\rf_model.joblib")

# Mongo connection
client = MongoClient("mongodb://localhost:27017/")
db = client["nids_db"]
collection = db["network_traffic"]

# UI
st.title("🚨 Network Intrusion Detection System")
st.markdown("Real-time prediction from MongoDB using a trained Random Forest model.")

# Fetch sample
# Fetch a random record from MongoDB
sample = collection.aggregate([{"$sample": {"size": 1}}]).next()
sample_df = pd.DataFrame([sample])
true_label = sample_df["label"].iloc[0]
sample_df.drop(columns=["_id"], inplace=True)

# Encode categorical columns
for col in sample_df.select_dtypes(include='object').columns:
    sample_df[col] = LabelEncoder().fit_transform(sample_df[col])

X_sample = sample_df.drop("label", axis=1)
pred = model.predict(X_sample)[0]

result = "Intrusion" if pred == 1 else "Normal"
actual = "Intrusion" if true_label == 1 else "Normal"

st.subheader(f"🔍 Prediction: {result}")
st.markdown(f"**True Label:** {actual}")
st.dataframe(sample_df)
