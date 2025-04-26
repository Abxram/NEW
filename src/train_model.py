import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
from mongo_utils import insert_data_to_mongo

# Load data
df = pd.read_csv("data\\NIDS_data.csv")

# Encode categorical features
label_encoders = {}
for col in df.select_dtypes(include='object').columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Split features/labels
X = df.drop("Label", axis=1)
y = df["Label"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
print(classification_report(y_test, clf.predict(X_test)))

# Save model
joblib.dump(clf, "model/rf_model.joblib")

# Save test data to MongoDB
test_data = X_test.copy()
test_data['label'] = y_test.values
insert_data_to_mongo(test_data, db_name='nids_db', collection_name='network_traffic')
