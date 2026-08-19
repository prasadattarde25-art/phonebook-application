<template>
  <div class="container">
    <h1>📱 Phonebook</h1>
    
    <!-- Add Contact Form -->
    <div class="add-contact">
      <h2>Add New Contact</h2>
      <form @submit.prevent="addContact">
        <div class="form-group">
          <input v-model="newContact.name" placeholder="Name" required />
          <input v-model="newContact.phone_number" placeholder="Phone Number" required />
          <input v-model="newContact.email" placeholder="Email" />
          <input v-model="newContact.address" placeholder="Address" />
          <button type="submit">Add Contact</button>
        </div>
      </form>
    </div>

    <!-- Contact List -->
    <div class="contact-list">
      <h2>Contact List</h2>
      <div v-if="loading">Loading...</div>
      <div v-if="error" class="error">{{ error }}</div>
      
      <table v-if="!loading && contacts.length > 0">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Phone Number</th>
            <th>Email</th>
            <th>Address</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="contact in contacts" :key="contact.id">
            <td>{{ contact.id }}</td>
            <td>
              <router-link :to="`/contact/${contact.id}`" class="contact-link">
                {{ contact.name }}
              </router-link>
            </td>
            <td>{{ contact.phone_number }}</td>
            <td>{{ contact.email || '-' }}</td>
            <td>{{ contact.address || '-' }}</td>
            <td>
              <button @click="deleteContact(contact.id)" class="delete-btn">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!loading && contacts.length === 0">No contacts found.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      contacts: [],
      loading: false,
      error: null,
      newContact: {
        name: '',
        phone_number: '',
        email: '',
        address: ''
      }
    }
  },
  mounted() {
    this.fetchContacts()
  },
  methods: {
    async fetchContacts() {
      this.loading = true
      try {
        const response = await axios.get('http://127.0.0.1:8000/contacts/')
        this.contacts = response.data
      } catch (err) {
        this.error = 'Failed to load contacts'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    async addContact() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/contacts/', this.newContact)
        this.contacts.push(response.data)
        this.newContact = { name: '', phone_number: '', email: '', address: '' }
      } catch (err) {
        alert('Failed to add contact')
        console.error(err)
      }
    },
    async deleteContact(id) {
      if (confirm('Are you sure you want to delete this contact?')) {
        try {
          await axios.delete(`http://127.0.0.1:8000/contacts/${id}`)
          this.contacts = this.contacts.filter(c => c.id !== id)
        } catch (err) {
          alert('Failed to delete contact')
          console.error(err)
        }
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 50px auto;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

h2 {
  color: #555;
  margin-bottom: 15px;
}

.add-contact {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.form-group {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr auto;
  gap: 10px;
}

.form-group input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.form-group button {
  padding: 10px 20px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.form-group button:hover {
  background: #218838;
}

.contact-list {
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

thead {
  background: #007bff;
  color: white;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

tbody tr:hover {
  background: #f1f3f5;
}

.contact-link {
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
}

.contact-link:hover {
  text-decoration: underline;
}

.delete-btn {
  padding: 5px 15px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.delete-btn:hover {
  background: #c82333;
}

.error {
  color: red;
  padding: 10px;
  background: #f8d7da;
  border-radius: 5px;
  margin: 10px 0;
}
</style>