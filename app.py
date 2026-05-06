from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get values
        study = float(request.form['study'])
        attendance = float(request.form['attendance'])
        marks = float(request.form['marks'])

        # Create DataFrame (IMPORTANT: same as training)
        data = pd.DataFrame([[study, attendance, marks]],
                            columns=['Study_Hours', 'Attendance', 'Previous_Marks'])

        # Prediction
        prediction = model.predict(data)[0]

        # Output
        result = "Pass" if prediction == 1 else "Fail"

        return render_template('index.html', 
                               prediction_text=f"Result: {result}",
                               study=study,
                               attendance=attendance,
                               marks=marks)

    except Exception as e:
        # Return inputs even on error
        study = request.form.get('study', '')
        attendance = request.form.get('attendance', '')
        marks = request.form.get('marks', '')
        return render_template('index.html', 
                               prediction_text=f"Error: {str(e)}",
                               study=study,
                               attendance=attendance,
                               marks=marks)

if __name__ == "__main__":
    app.run(debug=True)
