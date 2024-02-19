columns = ['id', 'Gender', 'Age', 'Height', 'Weight', 'family_history_with_overweight', 'FAVC', 'FCVC', 'NCP', 'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE', 'CALC', 'MTRANS', 'NObeyesdad']

sex = ["Male","Female"]

cat_cols = ['Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS', 'NObeyesdad']

num_cols = ['id', 'Age', 'Height', 'Weight', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']
yn_cols = ["family_history_with_overweight","FAVC","SCC"]

yn = ["yes","no"]

transport = ['Public_Transportation', 'Automobile', 'Walking', 'Motorbike', 'Bike']

unique_classes = ["Insufficient_Weight","Normal_Weight", "Overweight_Level_I","Overweight_Level_II","Overweight_Level_III","Obesity_Type_I","Obesity_Type_II","Obesity_Type_III"]  #Set the order here.

comments = {
    "Insufficient_Weight" : "Eat some food.",
    "Normal_Weight": "Kudos, Keep going the same way!",
    "Overweight_Level_I": "Watch your food!",
    "Overweight_Level_II" : "Start walking a bit",
    "Overweight_Level_III" : "",
    "Obesity_Type_I": "Hit the gym! Start healthy food only!",
    "Obesity_Type_II": "Gym, Healthy food and no junk at all!",
    "Obesity_Type_III": "DEFCON1! Go to the doctor!"
}