import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import ContactList from '../components/ContactList.vue'
import axios from 'axios'

vi.mock('axios')

describe('ContactList.vue', () => {

  beforeEach(() => {
    vi.clearAllMocks()

    axios.get.mockResolvedValue({
      data: {
        items: [
          {
            id: 1,
            name: 'Rahul Sharma',
            phone_number: '9876543210',
            email: 'rahul@example.com',
            address: 'Mumbai'
          },
          {
            id: 2,
            name: 'Amit Patil',
            phone_number: '9876543222',
            email: 'amit@example.com',
            address: 'Pune'
          }
        ],
        total: 2,
        page: 1,
        limit: 10,
        pages: 1
      }
    })
  })


  // ----------------------------------------
  // 1. Component renders
  // ----------------------------------------

  it('renders Phonebook title', async () => {
    const wrapper = mount(ContactList, {
      global: {
        stubs: {
          RouterLink: true
        }
      }
    })

    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.text()).toContain('Phonebook')
  })


  // ----------------------------------------
  // 2. Contacts load successfully
  // ----------------------------------------

  it('loads contacts from API', async () => {
    const wrapper = mount(ContactList, {
      global: {
        stubs: {
          RouterLink: true
        }
      }
    })

    await new Promise(resolve => setTimeout(resolve, 0))

    expect(axios.get).toHaveBeenCalled()

    expect(wrapper.text()).toContain('9876543210')
expect(wrapper.text()).toContain('9876543222')
expect(wrapper.text()).toContain('rahul@example.com')
expect(wrapper.text()).toContain('amit@example.com')
  })


  // ----------------------------------------
  // 3. Search functionality
  // ----------------------------------------

  it('searches contacts', async () => {
    const wrapper = mount(ContactList, {
      global: {
        stubs: {
          RouterLink: true
        }
      }
    })

    await new Promise(resolve => setTimeout(resolve, 0))

    const searchInput = wrapper.find('.search-input')

    await searchInput.setValue('Rahul')
    await searchInput.trigger('input')

    expect(axios.get).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/contacts/',
      {
        params: {
          search: 'Rahul',
          page: 1,
          limit: 10
        }
      }
    )
  })


  // ----------------------------------------
  // 4. Pagination - Next
  // ----------------------------------------

  it('moves to next page', async () => {

    axios.get.mockResolvedValue({
      data: {
        items: [
          {
            id: 11,
            name: 'Page Two Contact',
            phone_number: '9999999999',
            email: 'page2@example.com',
            address: 'Mumbai'
          }
        ],
        total: 11,
        page: 2,
        limit: 10,
        pages: 2
      }
    })

    const wrapper = mount(ContactList, {
      global: {
        stubs: {
          RouterLink: true
        }
      }
    })

    await new Promise(resolve => setTimeout(resolve, 0))

    // Force pagination state for testing
    wrapper.vm.totalPages = 2
    await wrapper.vm.$nextTick()

    const nextButton = wrapper
      .findAll('.pagination button')
      .find(button => button.text().includes('Next'))

    await nextButton.trigger('click')

    expect(wrapper.vm.currentPage).toBe(2)
  })


  // ----------------------------------------
  // 5. Pagination - Previous
  // ----------------------------------------

  it('moves to previous page', async () => {

    const wrapper = mount(ContactList, {
      global: {
        stubs: {
          RouterLink: true
        }
      }
    })

    await new Promise(resolve => setTimeout(resolve, 0))

    wrapper.vm.currentPage = 2
    wrapper.vm.totalPages = 2

    await wrapper.vm.$nextTick()

    const previousButton = wrapper
      .findAll('.pagination button')
      .find(button => button.text().includes('Previous'))

    await previousButton.trigger('click')

    expect(wrapper.vm.currentPage).toBe(1)
  })


  // ----------------------------------------
  // 6. Add contact
  // ----------------------------------------

  it('adds a new contact', async () => {

    axios.post.mockResolvedValue({
      data: {
        id: 3,
        name: 'New Contact',
        phone_number: '8888888888',
        email: 'new@example.com',
        address: 'Mumbai'
      }
    })

    const wrapper = mount(ContactList, {
      global: {
        stubs: {
          RouterLink: true
        }
      }
    })

    await new Promise(resolve => setTimeout(resolve, 0))

    wrapper.vm.newContact = {
      name: 'New Contact',
      phone_number: '8888888888',
      email: 'new@example.com',
      address: 'Mumbai'
    }

    await wrapper.vm.addContact()

    expect(axios.post).toHaveBeenCalled()

    expect(wrapper.vm.newContact.name).toBe('')
    expect(wrapper.vm.newContact.phone_number).toBe('')
  })


  // ----------------------------------------
  // 7. Delete contact
  // ----------------------------------------

  it('deletes a contact', async () => {

    global.confirm = vi.fn(() => true)

    axios.delete.mockResolvedValue({
      data: {
        message: 'Contact deleted successfully'
      }
    })

    const wrapper = mount(ContactList, {
      global: {
        stubs: {
          RouterLink: true
        }
      }
    })

    await new Promise(resolve => setTimeout(resolve, 0))

    await wrapper.vm.deleteContact(1)

    expect(axios.delete).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/contacts/1'
    )
  })

})