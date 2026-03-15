import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

real_news = [
"Government announces new healthcare policy",
"Scientists discover new exoplanet in distant galaxy",
"Stock market reaches record high this week",
"New education reforms approved by parliament",
"Researchers develop new cancer treatment",
"NASA launches satellite to study climate change",
"Economy grows faster than expected this quarter",
"Doctors discover new vaccine for virus",
"Technology company releases new AI chip",
"City government approves new public transport plan"
]

fake_news = [
"Aliens secretly living inside the earth core",
"Celebrity adopts invisible dragon as pet",
"Time traveler reveals future lottery numbers",
"Secret portal discovered in desert pyramid",
"Scientists confirm humans can breathe underwater soon",
"Ancient giants found sleeping under Antarctica",
"Government hiding alien technology from public",
"Man claims he can teleport using meditation",
"Moon made entirely of cheese says blogger",
"Dinosaurs spotted alive in remote jungle"
]

texts = []
labels = []

for _ in range(250):
    texts.append(random.choice(real_news))
    labels.append("Real")

for _ in range(250):
    texts.append(random.choice(fake_news))
    labels.append("Fake")

df = pd.DataFrame({
    "text":texts,
    "labels":labels
})

print("Data Size:", len(df))

vectorizer = TfidfVectorizer(stop_words="english")

x = vectorizer.fit_transform(df["text"])
y = df["labels"]

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

lr_model = LogisticRegression()
lr_model.fit(x_train,y_train)

rf_model = RandomForestClassifier()
rf_model.fit(x_train,y_train)

lr_pred = lr_model.predict(x_test)
rf_pred = rf_model.predict(x_test)

print("\nLogistic Regression Accuracy:",accuracy_score(y_test,lr_pred))
print("Random Forest Accuracy:",accuracy_score(y_test,rf_pred))

news = input("Enter the news: ")

vec = vectorizer.transform([news])

prediction = lr_model.predict(vec)

print("\nNews:",news)
print("Prediction:",prediction[0])


