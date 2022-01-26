import streamlit as st
import streamlit_authenticator as stauth
import requests
import json
from settings import *
APPLICATION_SERVICE_URL = "http://mt-aaa-be-api:5000/model/"
names = ['John Smith','Rebecca Briggs']
usernames = ['jsmith','rbriggs']
passwords = ['123','456']
print(REDIS_HOST)
# hashed_passwords = ['$2b$12$aQHnEmGfUTtauDP41PZTtObwLayhR3Nrui4PInymtv0J5OvjPYa4O',
#  '$2b$12$43.4ixYKxSr22wPj3HfGzum7pNO0IMMYkV6eOyXyT8WMFWsJJRhMK']
hashed_passwords = stauth.hasher(passwords).generate()

authenticator = stauth.authenticate(names,usernames,hashed_passwords,'some_cookie_name','some_signature_key',cookie_expiry_days=30)

name, authentication_status = authenticator.login('Login','main')

if authentication_status:
    st.write('Welcome *%s*' % (name))
    st.title('Some content')
    # Refresh model id list
    if st.button('Refresh model id list'):
        model_ids = requests.get(APPLICATION_SERVICE_URL + 'ids/').json()
        st.write(model_ids)
        st.write('model id list updated')
    # Submit model traning jobs
    submit_model_job = st.form(key="model-taining-trigger")
    model_name = submit_model_job.text_input("Enter model name")
    split_ratio = submit_model_job.text_input("Enter split ratio parameter")
    model_submit_event = submit_model_job.form_submit_button("Submit")
    if model_submit_event:
        model_train_data = {"model_name": model_name, "model_parameters": {"split_ratio": float(split_ratio)}}
        print(model_train_data)
        # TODO: Here status is not being updated in db
        r = requests.post(APPLICATION_SERVICE_URL + "train/", json=model_train_data)
        st.write(r.text)
    # Get model status
    get_model_status = st.form(key="model-status-check")
    model_ids = requests.get(APPLICATION_SERVICE_URL + 'ids/').json()
    selected_model_id_dict = get_model_status.selectbox('select model id',model_ids)
    model_status_check_event = get_model_status.form_submit_button("Submit")
    if model_status_check_event:
        selected_model_id = selected_model_id_dict['model_id']
        if selected_model_id == '12345':
            st.write('default model id selected')
        else:
            model_status_dict = requests.get(APPLICATION_SERVICE_URL + f'status/{selected_model_id}').json()
            st.write(model_status_dict)
    # Show model results
    get_model_results = st.form(key="model-result-check")
    model_ids = requests.get(APPLICATION_SERVICE_URL + 'ids/').json()
    selected_model_id__res_dict = get_model_results.selectbox('select model id',model_ids)
    model_result_get_event = get_model_results.form_submit_button("Submit")
    if model_result_get_event:
        selected_model_id_res = selected_model_id__res_dict['model_id']
        if selected_model_id_res == '12345':
            st.write('default model id selected')
        else:
            model_result_dict = requests.get(APPLICATION_SERVICE_URL + f'result/{selected_model_id_res}').json()
            st.write(model_result_dict)
    # Aggregated result
    get_aggregated_results = st.form(key="get-agg-results")
    model_ids = requests.get(APPLICATION_SERVICE_URL + 'ids/').json()
    selected_model_id_agg_dict = get_aggregated_results.selectbox('select model id',model_ids)
    agg_func = get_aggregated_results.text_input("Enter aggregation function")
    agg_result_get_event = get_aggregated_results.form_submit_button("Submit")
    if agg_result_get_event:
        selected_model_id_agg = selected_model_id_agg_dict['model_id']
        if selected_model_id_agg == '12345':
            st.write('default model id selected')
        else:
            model_agg_data = {"model_id": selected_model_id_agg, "agg_func": agg_func}
            r = requests.post(APPLICATION_SERVICE_URL + "aggregate/", json=model_agg_data)
            st.write(r.text)
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')