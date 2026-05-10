#!/usr/bin/python3

import json


def add_contact(contacts):
    name = input("Enter contact name: ")
    phone = input("Enter contact phone: ")
    email = input("Enter contact email: ")
    address = input("Enter contact address: ")
    for contact in contacts:
        if contact["name"].lower() == name.lower() and contact["phone"] == phone:
            print("Contact already exists.")
            return
    contacts.append({"name": name, "phone": phone, "email": email, "address": address})
    print("Contact added successfully.")    

def find_contact(contacts, name):
    result = []
    for contact in contacts:
        if contact["name"].lower() == name.lower():
            result.append(contact)
    return result

def choice_contact(contacts):
    name = input("Enter contact name: ")
    contacts = find_contact(contacts, name)
    if not contacts:
        print("Contact not found.")
        return
    elif len(contacts) == 1:
        return contacts[0]
    else:
        print("Multiple contacts found:")
        for i, contact in enumerate(contacts, start=1):
            print(f"{i}. {contact['name']} - {contact['phone']} - {contact['email']} - {contact['address']}")
        try:
            choice = int(input("Select a contact by number: "))
            if 1 <= choice <= len(contacts):
                return contacts[choice - 1]
            else:
                print("Invalid choice.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

def edit_contacts(contacts):
    contact = choice_contact(contacts)
    if not contact:
        return
    edit_choice = input("What do you want to edit? (phone/email/address): ")
    if edit_choice == "phone":
        phone = input("Enter new phone: ")
        contact["phone"] = phone
        print("Phone updated successfully.")
    elif edit_choice == "email":
        email = input("Enter new email: ")
        contact["email"] = email
        print("Email updated successfully.")
    elif edit_choice == "address":
        address = input("Enter new address: ")
        contact["address"] = address
        print("Address updated successfully.")
    else:
        print("Invalid choice.")


def view_contacts(contacts):
    if not contacts:
        print("No contacts to display.")
        return
    for contact in contacts:
        print(f"name:{contact['name']}, phone:{contact['phone']}, email:{contact['email']}, address:{contact['address']}") 
    
def search_contacts(contacts):
    contact = choice_contact(contacts)
    if contact:
        print(f"name:{contact['name']}, phone:{contact['phone']}, email:{contact['email']}, address:{contact['address']}")
    else:
        print("Contact not found.")

def delete_contact(contacts):
    contact = choice_contact(contacts)
    if contact:
        contacts.remove(contact)
        print("Contact deleted successfully.")
    else:
        print("Contact not found.")

def save_to_file(contacts):
    with open("contacts.json", "w") as file:
        json.dump(contacts, file, indent=4)

def load_from_file():
    try:
        with open("contacts.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def main():
    contacts = load_from_file()
    while True:
        print("\nContact Management System")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contacts")
        print("4. Edit Contacts")
        print("5. Delete Contact")
        print("6. Save and Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contacts(contacts)
        elif choice == "4":
            edit_contacts(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            save_to_file(contacts)
            print("Contacts saved. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
