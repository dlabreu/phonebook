mport React, { useState, useEffect } from 'react';

// Main App component
const App = () => {
  // State to store contacts
  const [contacts, setContacts] = useState([]);
  // State for the form input fields
  const [formData, setFormData] = useState({
    id: null,
    name: '',
    surname: '',
    company: '',
    phone: '',
    address: '',
  });
  // State for messages/notifications to the user
  const [message, setMessage] = useState('');
  // State to control message visibility
  const [showMessage, setShowMessage] = useState(false);

  // Simulate fetching contacts from an API on component mount
  useEffect(() => {
    // In a real application, you would make a fetch call here:
    // fetch('/api/contacts')
    //   .then(response => response.json())
    //   .then(data => setContacts(data))
    //   .catch(error => console.error('Error fetching contacts:', error));

    // For demonstration, use mock data
    const mockContacts = [
      { id: 1, name: 'John', surname: 'Doe', company: 'Acme Corp', phone: '123-456-7890', address: '123 Main St' },
      { id: 2, name: 'Jane', surname: 'Smith', company: 'Globex Inc', phone: '098-765-4321', address: '456 Oak Ave' },
      { id: 3, name: 'Peter', surname: 'Jones', company: 'Wayne Enterprises', phone: '555-123-4567', address: '789 Pine Ln' },
    ];
    setContacts(mockContacts);
  }, []);

  // Handle input changes for the form
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Display a message to the user
  const displayMessage = (msg) => {
    setMessage(msg);
    setShowMessage(true);
    setTimeout(() => {
      setShowMessage(false);
      setMessage('');
    }, 3000); // Message disappears after 3 seconds
  };

  // Handle form submission (add or update contact)
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.name || !formData.phone) {
      displayMessage('Name and Phone are required!');
      return;
    }

    if (formData.id) {
      // Update existing contact
      // In a real app: fetch(`/api/contacts/${formData.id}`, { method: 'PUT', body: JSON.stringify(formData) })
      const updatedContacts = contacts.map((contact) =>
        contact.id === formData.id ? { ...formData } : contact
      );
      setContacts(updatedContacts);
      displayMessage('Contact updated successfully!');
    } else {
      // Add new contact
      // In a real app: fetch('/api/contacts', { method: 'POST', body: JSON.stringify(formData) })
      const newContact = { ...formData, id: Date.now() }; // Generate a unique ID
      setContacts([...contacts, newContact]);
      displayMessage('Contact added successfully!');
    }
    // Clear form after submission
    setFormData({ id: null, name: '', surname: '', company: '', phone: '', address: '' });
  };

  // Handle editing a contact
  const handleEdit = (contact) => {
    setFormData({ ...contact });
  };

  // Handle deleting a contact
  const handleDelete = (id) => {
    // In a real app: fetch(`/api/contacts/${id}`, { method: 'DELETE' })
    if (window.confirm('Are you sure you want to delete this contact?')) {
      const filteredContacts = contacts.filter((contact) => contact.id !== id);
      setContacts(filteredContacts);
      displayMessage('Contact deleted successfully!');
    }
  };

  // Custom confirmation modal (instead of window.confirm)
  const CustomConfirmModal = ({ message, onConfirm, onCancel }) => (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-xl max-w-sm w-full">
        <p className="text-lg font-semibold mb-4 text-gray-800">{message}</p>
        <div className="flex justify-end space-x-3">
          <button
            onClick={onCancel}
            className="px-4 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400 transition duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-opacity-50"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );

  // State to manage the custom confirmation modal
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [contactToDeleteId, setContactToDeleteId] = useState(null);

  const confirmDelete = (id) => {
    setContactToDeleteId(id);
    setShowDeleteConfirm(true);
  };

  const handleConfirmDelete = () => {
    const filteredContacts = contacts.filter((contact) => contact.id !== contactToDeleteId);
    setContacts(filteredContacts);
    displayMessage('Contact deleted successfully!');
    setShowDeleteConfirm(false);
    setContactToDeleteId(null);
  };

  const handleCancelDelete = () => {
    setShowDeleteConfirm(false);
    setContactToDeleteId(null);
  };


  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 p-4 font-sans text-gray-900 flex flex-col items-center">
      <header className="w-full max-w-4xl bg-white p-6 rounded-xl shadow-lg mb-8 text-center">
        <h1 className="text-4xl font-extrabold text-indigo-700 mb-2 tracking-tight">
          📞 Phone Book App
        </h1>
        <p className="text-lg text-gray-600">Manage your contacts easily and efficiently.</p>
      </header>

      {/* Message Box */}
      {showMessage && (
        <div className="fixed top-4 left-1/2 -translate-x-1/2 bg-indigo-500 text-white px-6 py-3 rounded-full shadow-lg z-50 animate-fade-in-down">
          {message}
        </div>
      )}

      {/* Add/Edit Contact Form */}
      <section className="w-full max-w-4xl bg-white p-8 rounded-xl shadow-lg mb-8">
        <h2 className="text-3xl font-bold text-indigo-600 mb-6 text-center">
          {formData.id ? 'Edit Contact' : 'Add New Contact'}
        </h2>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
              Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="e.g., John"
              required
            />
          </div>
          <div>
            <label htmlFor="surname" className="block text-sm font-medium text-gray-700 mb-1">
              Surname
            </label>
            <input
              type="text"
              id="surname"
              name="surname"
              value={formData.surname}
              onChange={handleChange}
              className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="e.g., Doe"
            />
          </div>
          <div>
            <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-1">
              Company
            </label>
            <input
              type="text"
              id="company"
              name="company"
              value={formData.company}
              onChange={handleChange}
              className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="e.g., Acme Corp"
            />
          </div>
          <div>
            <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">
              Phone <span className="text-red-500">*</span>
            </label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="e.g., 123-456-7890"
              required
            />
          </div>
          <div className="md:col-span-2">
            <label htmlFor="address" className="block text-sm font-medium text-gray-700 mb-1">
              Address
            </label>
            <input
              type="text"
              id="address"
              name="address"
              value={formData.address}
              onChange={handleChange}
              className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="e.g., 123 Main St, Anytown"
            />
          </div>
          <div className="md:col-span-2 flex justify-center mt-4">
            <button
              type="submit"
              className="px-8 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition duration-300 ease-in-out transform hover:scale-105"
            >
              {formData.id ? 'Update Contact' : 'Add Contact'}
            </button>
            {formData.id && (
              <button
                type="button"
                onClick={() => setFormData({ id: null, name: '', surname: '', company: '', phone: '', address: '' })}
                className="ml-4 px-8 py-3 bg-gray-200 text-gray-800 font-semibold rounded-lg shadow-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition duration-300 ease-in-out transform hover:scale-105"
              >
                Cancel Edit
              </button>
            )}
          </div>
        </form>
      </section>

      {/* Contacts List */}
      <section className="w-full max-w-4xl bg-white p-8 rounded-xl shadow-lg">
        <h2 className="text-3xl font-bold text-indigo-600 mb-6 text-center">Your Contacts ({contacts.length})</h2>
        {contacts.length === 0 ? (
          <p className="text-center text-gray-500 text-lg">No contacts yet. Add some above!</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {contacts.map((contact) => (
              <div
                key={contact.id}
                className="bg-indigo-50 border border-indigo-200 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow duration-200 ease-in-out flex flex-col justify-between"
              >
                <div>
                  <h3 className="text-xl font-bold text-indigo-800 mb-2 truncate">
                    {contact.name} {contact.surname}
                  </h3>
                  {contact.company && (
                    <p className="text-gray-700 text-sm mb-1">
                      <span className="font-semibold">Company:</span> {contact.company}
                    </p>
                  )}
                  <p className="text-gray-700 text-sm mb-1">
                    <span className="font-semibold">Phone:</span> {contact.phone}
                  </p>
                  {contact.address && (
                    <p className="text-gray-700 text-sm">
                      <span className="font-semibold">Address:</span> {contact.address}
                    </p>
                  )}
                </div>
                <div className="flex justify-end gap-3 mt-4">
                  <button
                    onClick={() => handleEdit(contact)}
                    className="px-4 py-2 bg-purple-500 text-white rounded-lg shadow-md hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 transition-transform duration-200 ease-in-out transform hover:scale-105 text-sm"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => confirmDelete(contact.id)}
                    className="px-4 py-2 bg-red-500 text-white rounded-lg shadow-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-transform duration-200 ease-in-out transform hover:scale-105 text-sm"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
      {showDeleteConfirm && (
        <CustomConfirmModal
          message="Are you sure you want to delete this contact?"
          onConfirm={handleConfirmDelete}
          onCancel={handleCancelDelete}
        />
      )}
    </div>
  );
};

export default App;
