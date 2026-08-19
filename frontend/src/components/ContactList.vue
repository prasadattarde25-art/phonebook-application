```vue
<template>
  <div class="container">
    <h1>📱 Phonebook</h1>

    <!-- Add Contact Form -->
    <div class="add-contact">
      <h2>Add New Contact</h2>

      <form @submit.prevent="addContact">
        <div class="form-group">
          <input
            v-model="newContact.name"
            placeholder="Name"
            required
          />

          <input
            v-model="newContact.phone_number"
            placeholder="Phone Number"
            required
          />

          <input
            v-model="newContact.email"
            placeholder="Email"
            type="email"
          />

          <input
            v-model="newContact.address"
            placeholder="Address"
          />

          <button type="submit">
            Add Contact
          </button>
        </div>
      </form>
    </div>

    <!-- Contact List -->
    <div class="contact-list">

      <!-- Header + Search -->
      <div class="contact-header">
        <h2>Contact List</h2>

        <input
          v-model="searchQuery"
          @input="searchContacts"
          type="text"
          placeholder="🔍 Search contacts..."
          class="search-input"
        />
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading">
        Loading...
      </div>

      <!-- Error -->
      <div v-if="error" class="error">
        {{ error }}
      </div>

      <!-- Contact Table -->
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
          <tr
            v-for="contact in contacts"
            :key="contact.id"
          >
            <td>{{ contact.id }}</td>

            <td>
              <router-link
                :to="`/contact/${contact.id}`"
                class="contact-link"
              >
                {{ contact.name }}
              </router-link>
            </td>

            <td>{{ contact.phone_number }}</td>

            <td>
              {{ contact.email || '-' }}
            </td>

            <td>
              {{ contact.address || '-' }}
            </td>

            <td>
              <button
                @click="deleteContact(contact.id)"
                class="delete-btn"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <p
        v-if="!loading && contacts.length === 0"
        class="empty-message"
      >
        No contacts found.
      </p>

      <!-- Pagination -->
      <div
        v-if="!loading && totalPages > 1"
        class="pagination"
      >
        <button
          @click="previousPage"
          :disabled="currentPage === 1"
        >
          ← Previous
        </button>

        <span>
          Page {{ currentPage }} of {{ totalPages }}
        </span>

        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
        >
          Next →
        </button>
      </div>

    </div>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  data() {
    return {
      // Contacts
      contacts: [],

      // Loading & Error
      loading: false,
      error: null,

      // Search
      searchQuery: '',

      // Pagination
      currentPage: 1,
      totalPages: 1,
      pageSize: 10,

      // New Contact
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

    // ----------------------------------------
    // Fetch Contacts
    // ----------------------------------------

    async fetchContacts() {
      this.loading = true
      this.error = null

      try {
        const response = await axios.get(
          'http://127.0.0.1:8000/contacts/',
          {
            params: {
              search: this.searchQuery,
              page: this.currentPage,
              limit: this.pageSize
            }
          }
        )

        this.contacts = response.data.items
        this.totalPages = response.data.pages

      } catch (err) {
        this.error = 'Failed to load contacts'
        console.error(err)
      } finally {
        this.loading = false
      }
    },


    // ----------------------------------------
    // Search Contacts
    // ----------------------------------------

    async searchContacts() {
      this.currentPage = 1

      await this.fetchContacts()
    },


    // ----------------------------------------
    // Next Page
    // ----------------------------------------

    async nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++

        await this.fetchContacts()
      }
    },


    // ----------------------------------------
    // Previous Page
    // ----------------------------------------

    async previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--

        await this.fetchContacts()
      }
    },


    // ----------------------------------------
    // Add Contact
    // ----------------------------------------

    async addContact() {
      try {
        const response = await axios.post(
          'http://127.0.0.1:8000/contacts/',
          this.newContact
        )

        // Reset form
        this.newContact = {
          name: '',
          phone_number: '',
          email: '',
          address: ''
        }

        // Go to first page
        this.currentPage = 1

        // Refresh contact list
        await this.fetchContacts()

      } catch (err) {

        if (err.response && err.response.data) {
          alert(
            err.response.data.detail ||
            'Failed to add contact'
          )
        } else {
          alert('Failed to add contact')
        }

        console.error(err)
      }
    },


    // ----------------------------------------
    // Delete Contact
    // ----------------------------------------

    async deleteContact(id) {

      if (
        confirm(
          'Are you sure you want to delete this contact?'
        )
      ) {

        try {

          await axios.delete(
            `http://127.0.0.1:8000/contacts/${id}`
          )

          // Refresh current page
          await this.fetchContacts()

          // If current page becomes empty,
          // move to previous page
          if (
            this.contacts.length === 0 &&
            this.currentPage > 1
          ) {
            this.currentPage--

            await this.fetchContacts()
          }

        } catch (err) {

          if (err.response && err.response.data) {
            alert(
              err.response.data.detail ||
              'Failed to delete contact'
            )
          } else {
            alert('Failed to delete contact')
          }

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
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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


/* ----------------------------------------
   Add Contact
---------------------------------------- */

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


/* ----------------------------------------
   Contact List Header
---------------------------------------- */

.contact-list {
  margin-top: 20px;
}

.contact-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.contact-header h2 {
  margin-bottom: 0;
}

.search-input {
  width: 300px;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
}

.search-input:focus {
  border-color: #007bff;
}


/* ----------------------------------------
   Table
---------------------------------------- */

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

thead {
  background: #007bff;
  color: white;
}

th,
td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

tbody tr:hover {
  background: #f1f3f5;
}


/* ----------------------------------------
   Contact Link
---------------------------------------- */

.contact-link {
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
}

.contact-link:hover {
  text-decoration: underline;
}


/* ----------------------------------------
   Delete Button
---------------------------------------- */

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


/* ----------------------------------------
   Pagination
---------------------------------------- */

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 25px;
}

.pagination button {
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  background: #007bff;
  color: white;
  cursor: pointer;
  font-size: 14px;
}

.pagination button:hover:not(:disabled) {
  background: #0056b3;
}

.pagination button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.pagination span {
  font-weight: bold;
  color: #555;
}


/* ----------------------------------------
   Loading
---------------------------------------- */

.loading {
  text-align: center;
  padding: 20px;
  color: #007bff;
}


/* ----------------------------------------
   Error
---------------------------------------- */

.error {
  color: red;
  padding: 10px;
  background: #f8d7da;
  border-radius: 5px;
  margin: 10px 0;
}


/* ----------------------------------------
   Empty State
---------------------------------------- */

.empty-message {
  text-align: center;
  padding: 30px;
  color: #777;
}


/* ----------------------------------------
   Responsive Design
---------------------------------------- */

@media (max-width: 900px) {

  .form-group {
    grid-template-columns: 1fr 1fr;
  }

  .contact-header {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }

  .search-input {
    width: 100%;
    box-sizing: border-box;
  }

  table {
    font-size: 13px;
  }
}

@media (max-width: 600px) {

  .container {
    margin: 20px 10px;
    padding: 15px;
  }

  .form-group {
    grid-template-columns: 1fr;
  }

  table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }

  .pagination {
    gap: 10px;
  }
}

</style>
```
