import streamlit as st
import pandas as pd
import constants
from pickle import load
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler,OneHotEncoder

def data_sanity_check(df):

    #Check if the appropriate columns exist:
    for col in df:
        if col not in constants.columns:
            raise ValueError(f"Input file does not have a {col} column.")
    
    #Gender check:
    invalid_values = df[~df['Gender'].apply(lambda x: x.capitalize()).isin(constants.sex)][["id","Gender"]]    
    if not invalid_values.empty:        
        raise ValueError(f"Invalid Values found in Gender column for ids: {invalid_values['id'].tolist()}")
    

    # Numeric column check       
    for col in ['Age', 'Height', 'Weight', 'FCVC', 'NCP', 'CH2O']:
        try:
            # Convert the column to numeric (if it contains valid numeric values)
            df[col] = pd.to_numeric(df[col])
        except ValueError:
            # Handle any non-numeric values (e.g., strings, NaNs)
            print(f"Warning: {col} contains non-numeric values.")

        invalid_values = df[df[col].astype('float') <= 0]
        
        if not invalid_values.empty:
            raise ValueError(f"{col} cannot be 0 or negative.")
    
      
    for colname in constants.yn_cols:
        invalid_values = df[~df[colname].apply(lambda x: x.lower()).isin(constants.yn)][["id",colname]]
            
        if not invalid_values.empty:
            raise ValueError(f"Invalid Values found in {colname} column for ids: {invalid_values['id'].tolist()}")
       
    
    # MTRANS
    colname = "MTRANS"
    invalid_values = df[~df[colname].isin(constants.transport)][["id",colname]]
    if not invalid_values.empty:
        raise ValueError(f"Invalid Values found in{colname} column for ids: {invalid_values['id'].tolist()}")       


def generate_comments(df):    
    df["Comment"] = df["Status"].apply(lambda x: constants.comments.get(x))    
    return df

def convert_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def predict(data,model):    
    df = data.copy()
    df = df.drop(['id'],axis=1)
    X = df    
        
    preprocessor = ColumnTransformer([
    ('categorical_encoder', OneHotEncoder(drop='first'),constants.cat_cols),
    ('scaler', RobustScaler(with_centering=False),constants.num_cols)
    ])

    y_pred = model.predict(X)
    y_pred_decoded = [constants.unique_classes[i] for i in y_pred]

    result_df = pd.DataFrame({'Status': y_pred_decoded})

    # Concatenate the original features and the predicted target
    result_df = pd.concat([data, result_df], axis=1)

    # Generate Comments:
    result_df = generate_comments(result_df)   
    return result_df


def main():
    st.title("How obese are you?")

    input_file = st.file_uploader("Upload your excel file",type=["xlsx","csv"])

    if input_file is not None:
        # Get the file extension
        file_extension = input_file.name.split('.')[-1]

        if file_extension == 'csv':
            df = pd.read_csv(input_file)
        elif file_extension == 'xlsx':
            df = pd.read_excel(input_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            st.stop()           
    
    if st.button('Process File'):        
        if input_file is not None:
            data_sanity_check(df)
            st.success("File Processed successfully!")
        else:
            st.error("Please import your data.")
            st.stop()
    
        # Load the model:
        with open(r"models/rf_classifier.pkl","rb") as f: 
            rf_model = load(f)

    # Once the data sanity checks are passed, predict the result.
            result = predict(df,model=rf_model)
            result = result.iloc[:,[0,-2,-1]] #Keep Id and the result columns

        st.dataframe(result)
        csv_file = convert_to_csv(result)
                
        st.download_button(
            label= "Click Here to download data",
            data = csv_file,
            file_name= "Obesity Result.csv",
            mime='text/csv' 
        )
        
       
        
if __name__ == '__main__':
    main()