import streamlit as st
import requests

API_URL = "http://localhost:8000/api/todos"  # Replace this with your Django backend URL

def get_todos():
    response = requests.get(API_URL)
    return response.json()

def add_todo(title, description):
    data = {"title": title, "description": description}
    response = requests.post(API_URL, json=data)
    return response.json()

def mark_todo_as_completed(todo_id):
    url = f"{API_URL}/{todo_id}/complete"
    response = requests.patch(url)
    if response.content:
        return response.json()
    else:
        return {"message": "No content"}

def delete_todo(todo_id):
    url = f"{API_URL}/{todo_id}"
    response = requests.delete(url)
    if response.content:
        return response.json()
    else:
        return {"message": "No content"}

def main():
    st.title("Simple Todo App")

    # Display existing todos
    todos = get_todos()
    for todo in todos:
        todo_title = todo['title']
        todo_description = todo['description']
        todo_id = todo['id']
        completed = todo['completed']
        if completed:
            st.write(f"~~{todo_title}~~ - {todo_description} (Completed)")
        else:
            st.write(f"{todo_title} - {todo_description}")
        
        # Mark as completed button
        if not completed:
            if st.button(f"Mark as Completed: {todo_title}"):
                mark_todo_as_completed(todo_id)
                st.success(f"Todo '{todo_title}' marked as completed!")

        # Delete button
        if st.button(f"Delete: {todo_title}"):
            delete_todo(todo_id)
            st.success(f"Todo '{todo_title}' deleted successfully!")

    # Add new todo
    st.subheader("Add New Todo")
    new_title = st.text_input("Title:")
    new_description = st.text_input("Description:")
    if st.button("Add"):
        add_todo(new_title, new_description)
        st.success("Todo added successfully!")

if __name__ == "__main__":
    main()
