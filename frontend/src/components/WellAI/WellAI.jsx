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
        { sender: "bot", text: "Error connecting to the server." },
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
        <h1 className="chat-title">🩺 WellWise Health Chatbot</h1>

        <div className="messages">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`message ${msg.sender === "user" ? "user" : "bot"}`}
            >
              {msg.sender === "bot" ? (
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeHighlight]}
                  components={{
                    a: (props) => (
                      <a
                        {...props}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="markdown-link"
                      />
                    ),
                    code: ({ inline, className, children, ...props }) => (
                      <code
                        className={`${
                          inline ? "inline-code" : "block-code"
                        } ${className || ""}`}
                        {...props}
                      >
                        {children}
                      </code>
                    ),
                  }}
                >
                  {msg.text}
                </ReactMarkdown>
              ) : (
                msg.text
              )}
            </div>
          ))}

          {loading && <div className="loading">AI is thinking...</div>}
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
            Send
          </button>
        </div>

        <button className="clear-btn" onClick={clearChat}>
          Clear Chat
        </button>
      </div>
    </div>
  );
}
