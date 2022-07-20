Run the application locally:

1. Add the excel file "raw_datas_projet_M5D_Hetic.xlsx" in the [src/data](src/data/) folder.
2. Download the json file "correspondance-code-insee-code-postal.json" from [opendata](https://public.opendatasoft.com/explore/dataset/correspondance-code-insee-code-postal/export/) and add it in the [src/data](src/data/) folder.
3. Add a "secrets.yml" with your own credentials in the [secretdir](secretdir/) folder, following the [example](secretdir/secrets.yml.example)
2. Install pipenv if not yet installed: `pip install pipenv`
3. Create a virtual environment: `pipenv install`
4. Enter the virtual environment: `pipenv shell`
5. Launch the Streamlit application: `streamlit run src/frontend/🏘️Home.py`

Deployed application: https://castorama-reviews.herokuapp.com/

Mockup: https://www.figma.com/file/9FLIPKBf3N1cBSDKmZH9m6/Castorama?node-id=0%3A1

Team planning: https://miro.com/app/board/uXjVOniXd3s=/