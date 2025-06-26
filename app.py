import React, { useState, useEffect } from 'react';

// Main App component for the even simpler Phone Book (display-only)
const App = () => {
  // IMPORTANT: Replace this with the actual URL of your Flask backend.
  // This could be your VM's IP address and port (e.g., 'http://YOUR_VM_IP:5000')
  // or your OpenShift route URL (e.g., 'http://my-phonebook-backend.apps.myopenshift.com')
  const BACKEND_URL = 'http://localhost:5000'; // Default for local testing, CHANGE THIS!

  // State to store contacts (only name and phone now)
  const [contacts, setContacts] = useState([]);
  // State for messages/notifications to the user
  const [message, setMessage] = useState('');
  // State to control message visibility
  const [showMessage, setShowMessage] = useState(false);

  // Function to fetch contacts from the backend API
  const fetchContacts = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/contacts`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setContacts(data);
    } catch (error) {
      console.error('Error fetching contacts:', error);
      displayMessage('Failed to load contacts.');
    }
  };

  // Fetch contacts on component mount
  useEffect(() => {
    fetchContacts();
  }, []);

  // Display a message to the user
  const displayMessage = (msg) => {
    setMessage(msg);
    setShowMessage(true);
    setTimeout(() => {
      setShowMessage(false);
      setMessage('');
    }, 3000); // Message disappears after 3 seconds
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 p-4 font-sans text-gray-900 flex flex-col items-center">
      <header className="w-full max-w-4xl bg-white p-6 rounded-xl shadow-lg mb-8 text-center">
        <h1 className="text-4xl font-extrabold text-indigo-700 mb-2 tracking-tight">
          📞 Simple Phone Book Viewer
        </h1>
        <p className="text-lg text-gray-600">View contacts from the backend.</p>
      </header>

      {/* Message Box */}
      {showMessage && (
        <div className="fixed top-4 left-1/2 -translate-x-1/2 bg-indigo-500 text-white px-6 py-3 rounded-full shadow-lg z-50 animate-fade-in-down">
          {message}
        </div>
      )}

      {/* Contacts List */}
      <section className="w-full max-w-4xl bg-white p-8 rounded-xl shadow-lg">
        <h2 className="text-3xl font-bold text-indigo-600 mb-6 text-center">Your Contacts ({contacts.length})</h2>
        {contacts.length === 0 ? (
          <p className="text-center text-gray-500 text-lg">No contacts yet. Ensure backend is running and connected.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {contacts.map((contact) => (
              <div
                key={contact.id}
                className="bg-indigo-50 border border-indigo-200 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow duration-200 ease-in-out flex flex-col justify-between"
              >
                <div>
                  <h3 className="text-xl font-bold text-indigo-800 mb-2 truncate">
                    {contact.name}
                  </h3>
                  <p className="text-gray-700 text-sm mb-1">
                    <span className="font-semibold">Phone:</span> {contact.phone}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
};

export default App;

