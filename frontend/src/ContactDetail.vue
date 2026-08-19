<template>
  <div class="container">
    <button @click="goBack" class="back-btn">← Back to Contacts</button>
    
    <h1>📱 Contact Details</h1>
    
    <div v-if="loading" class="loading">Loading contact...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="!loading && contact" class="contact-card">
      <h2>{{ contact.name }}</h2>
      
      <div class="detail-row">
        <strong>Phone Number:</strong>
        <span>{{ contact.phone_number }}</span>
      </div>
      
      <div class="detail-row">
        <strong>Email:</strong>
        <span>{{ contact.email || '-' }}</span>
      </div>
      
      <div class="detail-row">
        <strong>Address:</strong>
        <span>{{ contact.address || '-' }}</span>
      </div>
      
      <div class="detail-row">
        <strong>ID:</strong>
        <span>{{ contact.id }}</span>
      </div>

      <button @click="toggleEdit" class="update-btn">
        {{ isEditing ? 'Cancel Edit' : 'Update' }}
      </button>

      <div v-if="isEditing" class="edit-form">
        <h3>Edit Contact</h3>
        <form @submit.prevent="updateContact">
          <div class="form-group">
            <input v-model="editForm.name" placeholder="Name" required />
            <input v-model="editForm.phone_number" placeholder="Phone" required />
            <input v-model="editForm.email" placeholder="Email" />
            <input v-model="editForm.address" placeholder="Address" />
          </div>
          <div class="button-group">
            <button type="submit" class="save-btn">Save Changes</button>
            <button type="button" @click="toggleEdit" class="cancel-btn">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      contact: null,
      loading: true,
      error: null,
      isEditing: false,
      editForm: {
        name: '',
        phone_number: '',
        email: '',
        address: ''
      }
    }
  },
  mounted() {
    this.fetchContact()
  },
  methods: {
    async fetchContact() {
      const id = this.$route.params.id
      console.log('📞 Contact ID:', id)
      
      try {
        const response = await axios.get(`http://127.0.0.1:8000/contacts/${id}`)
        this.contact = response.data
        this.editForm = { ...response.data }
        console.log('✅ Contact data:', response.data)
      } catch (err) {
        this.error = '❌ Failed to load contact'
        console.error('Error:', err)
      } finally {
        this.loading = false
      }
    },
    goBack() {
      this.$router.push('/')
    },
    toggleEdit() {
      this.isEditing = !this.isEditing
      if (!this.isEditing) {
        this.editForm = { ...this.contact }
      }
    },
    async updateContact() {
      try {
        const response = await axios.put(
          `http://127.0.0.1:8000/contacts/${this.contact.id}`,
          this.editForm
        )
        this.contact = response.data
        this.isEditing = false
        alert('✅ Contact updated successfully!')
      } catch (err) {
        alert('❌ Failed to update contact')
        console.error(err)
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.back-btn {
  background: #333;
  color: white;
  padding: 10px 18px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
}

.back-btn:hover {
  background: #555;
}

.contact-card {
  background: white;
  padding: 30px;
  border-radius: 8px;
}

.contact-card h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 24px;
}

.detail-row {
  display: flex;
  padding: 15px;
  border-bottom: 1px solid #ddd;
  font-size: 17px;
}

.detail-row strong {
  width: 180px;
  color: #333;
}

.detail-row span {
  color: #555;
}

.update-btn {
  display: block;
  margin: 30px auto 0;
  padding: 12px 30px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.update-btn:hover {
  background: #0056b3;
}

.edit-form {
  margin-top: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.edit-form h3 {
  margin-bottom: 15px;
  color: #333;
}

.form-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 15px;
}

.form-group input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.button-group {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.save-btn {
  padding: 10px 30px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.save-btn:hover {
  background: #218838;
}

.cancel-btn {
  padding: 10px 30px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.cancel-btn:hover {
  background: #c82333;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #666;
}

.error {
  text-align: center;
  padding: 20px;
  font-size: 18px;
  color: red;
  background: #f8d7da;
  border-radius: 5px;
}
</style>