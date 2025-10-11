import React, { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import "highlight.js/styles/github.css";
import "./WellAI.css";

export default function WellAI() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("https://nicholas-unmilitarised-matteo.ngrok-free.dev//chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();
      const botMsg = {
        sender: "bot",
        text: data.reply || "Sorry, I couldn’t generate a response.",
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error("Error:", err);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ Error connecting to the server." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="chat-wrapper">
      <div className="chat-box">
        <div className="chat-header">
          <img
            src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
            alt="bot"
            className="bot-logo"
          />
          <h1 className="chat-title">WellWise Health Assistant</h1>
        </div>

        <div className="messages">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`message-row ${
                msg.sender === "user" ? "user-row" : "bot-row"
              }`}
            >
              {msg.sender === "bot" && (
                <img
                  src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
                  alt="bot"
                  className="avatar"
                />
              )}
              <div className={`message ${msg.sender}`}>
                {msg.sender === "bot" ? (
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    rehypePlugins={[rehypeHighlight]}
                  >
                    {msg.text}
                  </ReactMarkdown>
                ) : (
                  msg.text
                )}
              </div>
              {msg.sender === "user" && (
                <img
                  src="https://cdn-icons-png.flaticon.com/512/1077/1077012.png"
                  alt="user"
                  className="avatar"
                />
              )}
            </div>
          ))}

          {loading && <div className="loading">💭 AI is thinking...</div>}
          <div ref={chatEndRef} />
        </div>

        <div className="input-section">
          <input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
          />
          <button onClick={sendMessage} disabled={loading}>
            ➤
          </button>
        </div>

        <button className="clear-btn" onClick={clearChat}>
          🧹 Clear Chat
        </button>
      </div>
    </div>
  );
}
