from bottle import Bottle, request, run, template, static_file
import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
import tracemalloc
tracemalloc.start()


app = Bottle()

def load_model_and_data():
    # Load training data
    df = pd.read_csv("Training.csv")
    # Load testing data
    tr = pd.read_csv("Testing.csv")

    # List of symptoms
    l1 = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
          'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
          'spotting_urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings',
          'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever',
          'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin',
          'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation',
          'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure',
          'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision',
          'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain',
          'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
          'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
          'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties',
          'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain',
          'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness',
          'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell',
          'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching',
          'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body',
          'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite',
          'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances',
          'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding',
          'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum',
          'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring',
          'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister',
          'red_sore_around_nose', 'yellow_crust_ooze']

    # List of diseases
    disease = ['Fungal infection', 'Allergy', 'GERD', 'Chroniccholestasis', 'DrugReaction', 'Peptic ulcer diseae', 'AIDS',
               'Diabetes', 'Gastroenteritis', 'BronchialAsthma', 'Hypertension', ' Migraine', 'Cervicalspondylosis',
               'Paralysis (brain hemorrhage)', 'Jaundice', 'Malaria', 'Chickenpox', 'Dengue', 'Typhoid', 'hepatitisA',
               'HepatitisB', 'HepatitisC', 'Hepatitis D', 'Hepatitis E', 'Alcoholichepatitis', 'Tuberculosis',
               'CommonCold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)', 'Heartattack', 'Varicoseveins',
               'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis', 'Arthritis',
               '(vertigo) Paroymsal  Positional Vertigo', 'Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']

    # Normalize the values in the 'prognosis' column to match with the 'disease' list
    df['prognosis'] = df['prognosis'].apply(lambda x: x.title())  # Convert to title case
    df['prognosis'] = df['prognosis'].replace({'Peptic Ulcer Diseae': 'Peptic ulcer diseae'})  # Correct typo

    # Convert labels to integers
    df['prognosis'] = df['prognosis'].apply(lambda x: disease.index(x) if x in disease else -1)  # Handle missing values

    # Filter out rows with missing or unknown diseases (-1)
    df = df[df['prognosis'] != -1]

    X = df[l1]
    y = df["prognosis"]

    # Load testing data
    tr = pd.read_csv("Testing.csv")
    tr['prognosis'] = tr['prognosis'].apply(lambda x: x.title())  # Convert to title case
    tr['prognosis'] = tr['prognosis'].replace({'Peptic Ulcer Diseae': 'Peptic ulcer diseae'}) 
    # Correct typo
    tr['prognosis'] = tr['prognosis'].apply(lambda x: disease.index(x) if x in disease else -1)  # Handle missing
    tr = tr[tr['prognosis'] != -1] # Filter out rows with missing or unknown diseases (-1)
    X_test = tr[l1]
    y_test = tr["prognosis"]

    gnb = MultinomialNB()
    gnb.fit(X, np.ravel(y))

    return gnb, l1, disease

def predict_disease(symptoms):
    gnb, l1, disease = load_model_and_data()
    l2 = [0] * len(l1)
    for k in range(0, len(l1)):
        for z in symptoms:
            if z == l1[k]:
                l2[k] = 1

    inputtest = [l2]
    predict = gnb.predict(inputtest)
    predicted = predict[0]
    predicted_disease = disease[predicted]
    print(predicted_disease)
    return predicted_disease
    
@app.route('/')
def index():
    # Return index.html template
    form = """
    <head>
    <title>MEDICHECK</title>
    <link rel="icon" type="image/x-icon" href="img/1.png"/>
    <meta property="og:title" content="Inexperienced Alienated Gerbil" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta charset="utf-8" />

    <meta property="twitter:card" content="summary_large_image" />
    <style>
        /* General styles */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Cabin:ital,wght@0,400..700;1,400..700&display=swap');
        body {
            font-family: 'Poppins', sans-serif;
            background: #fff;
            /* background: rgb(53, 69, 43);
            background: linear-gradient(90deg, rgba(53, 69, 43, 1) 0%, rgba(118, 131, 80, 1) 100%); */
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 600px;
            margin: 90px auto;
            /* background: #fff; */
            padding: 20px;
            background: rgb(53, 69, 43);
            background: linear-gradient(90deg, rgba(53, 69, 43, 1) 0%, rgba(118, 131, 80, 1) 100%);
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        
        h1 {
            text-align: center;
            color: #fff;
        }

        form {
            margin-top: 20px;
        }

        label {
            color: #fff;
            display: block;
            margin-bottom: 8px;
        }

        input[type="text"],
        input[type="password"],
        select {
            
            font-size: 15px;
            font-family: 'Poppins', sans-serif;
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
            background-color: rgba(255, 255, 255, 0.7);
        }

        input[type="submit"] {
            border: 2px solid #fff;
            font-family: 'Poppins', sans-serif;
            background: rgb(53, 69, 43);
            background: linear-gradient(90deg, rgba(53, 69, 43, 1) 0%, rgba(118, 131, 80, 1) 100%);
            color: #fff;
            
            border-radius: 5px;
            padding: 12px 20px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
            width: 100%;
        }

        input[type="submit"]:hover {
            background: linear-gradient(90deg, rgba(53, 69, 43, 1) 0%, rgba(118, 131, 80, 1) 100%);
        }

        .error-message {
            color: red;
            margin-top: 5px;
        }
        .medi {
    position: absolute;
    top: -14px; /* Adjust this value to set the distance from the top */
    left: 8px; /* Adjust this value to set the distance from the left */
    display: flex;
    align-items: center;
    padding: 40px;
}

.logo {
    font-size: 2em;
    font-family: Cabin;
    font-weight: 700;
    line-height: 150%;
    text-transform: uppercase;
    padding-inline: 4px;
    letter-spacing: 2.5px;
    color: inherit;
    text-decoration: inherit;
    
}

    </style>
</head>
<body>
<div class="container">
    <form action="/predict" method="post" onsubmit="return validateForm()">
        <h1>Select Symptoms</h1>
        <label for="symptom1">Symptom 1:</label>
        <select name="symptom1" id="symptom1"></select>
        <label for="symptom2">Symptom 2:</label>
        <select name="symptom2" id="symptom2"></select>
        <label for="symptom3">Symptom 3:</label>
        <select name="symptom3" id="symptom3"></select>
        <label for="symptom4">Symptom 4:</label>
        <select name="symptom4" id="symptom4"></select>
        <label for="symptom5">Symptom 5:</label>
        <select name="symptom5" id="symptom5"></select>
        <input type="submit" value="Predict">
    </form>
</div>
    <script>
        var symptoms = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
            'spotting_urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever',
            'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation',
            'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision',
            'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
            'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties',
            'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness',
            'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching',
            'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite',
            'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding',
            'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring',
            'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze'];

        // Sort symptoms alphabetically
        symptoms.sort();

        // Function to populate dropdowns
        function populateDropdowns() {
            for (var i = 1; i <= 5; i++) {
                var select = document.getElementById('symptom' + i);
                // Add default "Select Symptom" option
                var defaultOption = document.createElement('option');
                defaultOption.text = 'Select Symptom';
                defaultOption.value = '';
                select.appendChild(defaultOption);
                for (var j = 0; j < symptoms.length; j++) {
                    var option = document.createElement('option');
                    option.value = symptoms[j];
                    option.text = symptoms[j];
                    select.appendChild(option);
                }
            }
        }

        // Call the function to populate dropdowns
        populateDropdowns();

        // Function to validate form submission
        function validateForm() {
            var symptom1 = document.getElementById("symptom1").value;
            var symptom2 = document.getElementById("symptom2").value;
            var symptom3 = document.getElementById("symptom3").value;
            var symptom4 = document.getElementById("symptom4").value;
            var symptom5 = document.getElementById("symptom5").value;

            // Check if all fields are filled
            if (symptom1 === "" || symptom2 === "" || symptom3 === "" || symptom4 === "" || symptom5 === "") {
                alert("Please fill in all symptom fields.");
                return false; // Prevent form submission
            }
            return true; // Allow form submission
        }
    </script>
</body>


    """
    return form

@app.route('/predict.html', method=['GET', 'POST'])
def predict_html():
    return static_file('predict.html', root='C:/xampp/htdocs/My Project')



@app.route('/predict', method='POST')
def predict():
    selected_symptoms = [request.forms.get(f"symptom{i}") for i in range(1, 6)]  # Assuming 5 symptoms
    predicted_disease = predict_disease(selected_symptoms)
    print("Predicted Disease:", predicted_disease) 
    return template('predict', predicted_disease=predicted_disease)

if __name__ == "__main__":
    run(app, host='localhost', port=5501, debug=True)

