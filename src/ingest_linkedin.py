import pandas as pd
import os

BASE_PATH="data/raw/linkedin"
OUTPUT_FILE="data/processed/linkedin_cleaned.txt"

def process_all_linkedin_files():
    
    final_text=""

    #Loop through all CSV files
    for file in os.listdir(BASE_PATH):
        if file.endswith(".csv"):
            file_path=os.path.join(BASE_PATH,file)

            try:
                df=pd.read_csv(file_path)
            except Exception as e:
                print(f"Error reading {file}:{e}")
                continue

            #Main heading = file name
            section_name=file.replace(".csv","").upper()
            final_text+=f"\n\n========SECTION: {section_name}==========\n"

            #Skip empty files
            if df.empty:
                final_text+="No data available\n"
                continue

            #Process each row
            for _,row in df.iterrows():
                final_text+="\n"

                for col in df.columns:
                    value=str(row.get(col,"")).strip()

                    if value and value.lower()!="nan":
                        final_text+=f"{col}:{value}\n"
        
    #save output
    with open(OUTPUT_FILE,"w",encoding="utf-8") as f:
        f.write(final_text)
        
    print("Linkedin data processed successfully...")

if __name__=="__main__":
    process_all_linkedin_files()


