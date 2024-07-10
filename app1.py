import streamlit as st
import pickle
from keras.utils import pad_sequences
import numpy as np

st.title("Parts of Speech Tags")

with st.sidebar:
    pages = st.radio('Pages', ['Home', 'Page_1'])

# Global variables to store input and POS results
if 'inp_list' not in st.session_state:
    st.session_state['inp_list'] = []
if 'pos_result_list' not in st.session_state:
    st.session_state['pos_result_list'] = []

def home():
    inp = st.text_input("Enter a string")
    submit_btn = st.button("Submit")
    if submit_btn and inp:
        model = pickle.load(open(r"C:\Users\LENOVO\Desktop\POS tag\model.pkl", "rb"))
        tk_x = pickle.load(open(r"C:\Users\LENOVO\Desktop\POS tag\tk_x.pkl", "rb"))
        tk_y = pickle.load(open(r"C:\Users\LENOVO\Desktop\POS tag\tk_y.pkl", "rb"))

        def pos_tags(inp):
            seq = tk_x.texts_to_sequences([inp])
            text = tk_x.sequences_to_texts(seq)
            st.subheader("Tokenized input")
            for i in text:
                st.subheader(i)
            x = pad_sequences(seq, maxlen=271, padding='post')
            seqs = np.argmax(model.predict(x)[0], axis=1)[np.argmax(model.predict(x)[0], axis=1) != 0]
            pos = tk_y.sequences_to_texts([seqs])
            st.subheader('POS TAGS')
            for j in pos:
                return j

        st.session_state['inp_list'] = inp.split()  # Store the input list in the session state
        st.session_state['pos_result_list'] = pos_tags(st.session_state['inp_list']).split()  # Store the POS results in the session state
        st.subheader(" ".join(st.session_state['pos_result_list']))

def Page1():
    if st.session_state['inp_list']:
        word = st.text_input("Enter a word from the sequence")
        sub_btn = st.button("Submit")

        if word and sub_btn:
            if word in st.session_state['inp_list']:
                i = st.session_state['inp_list'].index(word)
                pos_tag = st.session_state['pos_result_list'][i]
                st.subheader(pos_tag)
            else:
                st.subheader("Enter a word that is in the sequence")
    else:
        st.subheader("Go to the Home page and input a sequence first")

if pages == 'Home':
    home()

if pages == 'Page_1':
    Page1()