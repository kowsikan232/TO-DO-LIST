import streamlit as st
from pymongo import MongoClient
client = MongoClient("mongodb+srv://kowsikan:goat@cluster0.ayjhj.mongodb.net/")
db = client['TodoList']
collection = db['UserNames']

def getnames():
    return list(collection.find())

def nametodatabase(name):
    collection.insert_one({"name": name})

def modify(name_id, new_name):
    collection.update_one({"_id": name_id}, {"$set": {"name": new_name}})

def delete(name_id):
    collection.delete_one({"_id": name_id})

def addname():
    name = st.text_input("Enter a name to add:")
    if st.button("Add Name"):
        if name:
            nametodatabase(name)
            st.success(f"Added name: {name}")
        else:
            st.error("Name cannot be empty")

def modifyname():
    names = getnames()
    if not names:
        st.warning("No names to modify")
        return
    
    name_id = st.selectbox("Select a name to modify:", names, format_func=lambda x: x['name'])
    new_name = st.text_input("Enter the new name:")
    
    if st.button("Modify Name"):
        if new_name:
            modify(name_id['_id'], new_name)
            st.success(f"Modified name to {new_name}")
        else:
            st.error("New name cannot be empty")

def deletename():
    names = getnames()
    if not names:
        st.warning("No names to delete")
        return
    
    name_id = st.selectbox("Select a name to delete:", names, format_func=lambda x: x['name'])
    
    if st.button("Delete Name"):
        delete(name_id['_id'])
        st.success(f"Deleted name")

st.title("TodoList")
option = st.radio("Choose an option", ["Add Name", "Modify Name", "Delete Name"])

if option == "Add Name":
    addname()
elif option == "Modify Name":
    modifyname()
elif option == "Delete Name":
    deletename()

st.subheader("Current Names")
names = getnames()
for name in names:
    st.write(f"{name['name']}")
