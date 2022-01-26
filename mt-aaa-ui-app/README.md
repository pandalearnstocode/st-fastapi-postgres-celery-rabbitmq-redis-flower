```bash
conda create --name mt-aaa-ui-app python=3.8
conda activate mt-aaa-ui-app
# conda deactivate
cd mt-aaa-ui-app/
pip install -r requirements.txt
```

## TODO:

* login
  * input
    * user name: string
    * password: string
  * output
    * status: integer
* get all model ids
  * output
    * dict of all model ids, name & status in a nested json, where 1st level key is model name and values is a dict with model id, model status, model name and model parameters.
      * model name: string
        * model id: string
        * model status: string
        * model name: string
        * model parameters: Dict{str,str}
* submit a model training job
  * input
    * model name: string
    * model parameters : dict
  * output
    * model name : string
    * model id : string
    * model status : string
* get status of a model training job
  * input
    * model id : string
  * output
    * model name : string
    * model status : string
    * model id : string
* view results for a model training job
  * input
    * model id : string
  * output
    * model name : string
    * model status : string
    * model id : string
    * model results : string
* aggregate results of a existing model
  * input
    * model id : string
    * aggregation level : string
    * aggregation function : string
  * output
    * model id : string
    * aggregated results : dict
* visualize results for a existing model (optional)
  * input
    * model id : string
    * visualization type : string
  * output
    * svg/png/jpg/html+css


## Reference:
* https://medium.com/artificialis/how-to-add-user-authentication-on-your-streamlit-app-c7f50c085b9f
* https://github.com/mkhorasani/Streamlit-Authenticator
* https://github.com/anarinsk/test-streamlit-authenticator/blob/main/app.py