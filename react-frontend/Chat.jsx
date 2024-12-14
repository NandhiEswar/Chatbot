import React, { useState } from 'react';
import axios from 'axios';
import { RingLoader } from 'react-spinners'; // Import the spinner from react-spinners

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false); // State to track if request is loading

  const sendMessage = async () => {
    if (input.trim() === '') return;

    // Set loading state to true before sending the request
    setLoading(true);

    try {
      // Send text to Flask server for summarization
      const response = await axios.post(`http://127.0.0.1:5000/values?query=${input}`,{ query: input });
      const summarizedText = response.data.summary;

      // Add both user message and summary to the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'User', text: input },
        { sender: 'Bot', text: summarizedText },
      ]);
      setInput('');
    } catch (error) {
      console.error('Error summarizing text:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'Error', text: 'Failed to summarize the text' },
      ]);
    } finally {
      // Set loading state to false once the request completes
      setLoading(false);
    }
  };

  return (
    <div className="h-screen bg-gray-100 mt-20 md:mt-8 flex items-center justify-center">
      <div className="w-full h-screen bg-white shadow-lg rounded-lg p-6">
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-4">
          Chat with Summarization
        </h1>
        <div
          id="chat-window"
          className="h-[520px] bg-gray-200 p-4 rounded-lg overflow-y-auto mb-4"
        >
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`p-2 rounded-lg mb-2 ${
                msg.sender === 'User' ? 'bg-blue-100 text-gray-800' : 'bg-green-100 text-gray-800'
              }`}
            >
              <strong>{msg.sender}: </strong>{msg.text}
            </div>
          ))}
        </div>

        {/* Loading spinner */}
        {loading && (
          <div className="flex justify-center items-center mb-4">
            <RingLoader color="#3498db" size={50} />
          </div>
        )}

        <div className="flex items-center space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-2 border border-gray-300 rounded-lg"
          />
          <button
            onClick={sendMessage}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
