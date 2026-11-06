from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Nexura Rule-Based Chatbot API", version="1.0")

class RuleBasedChatbot:
    def __init__(self):
        self.decision_tree = {
            "start_node": {
                "message": "مرحباً بك في شركة Nexura Solutions! 🚀\nكيف يمكننا مساعدتك اليوم؟ اختر من القائمة التالية:",
                "buttons": {
                    "1": {"text": "عرض الخدمات المتاحة", "next_node": "services_node"},
                    "2": {"text": "الأسئلة الشائعة (FAQs)", "next_node": "faqs_node"},
                    "3": {"text": "التواصل مع الدعم الفني", "next_node": "contact_node"},
                    "4": {"text": "إنهاء المحادثة", "next_node": "exit_node"}
                }
            },
            "services_node": {
                "message": "إليك الخدمات والحلول البرمجية المتوفرة لدينا:\n• Generative AI Chatbots\n• RAG Chatbots\n• Intent-Based Chatbots\n• Rule-Based Chatbots",
                "buttons": {
                    "1": {"text": "العودة للقائمة الرئيسية", "next_node": "start_node"},
                    "2": {"text": "التواصل مع الدعم الفني", "next_node": "contact_node"}
                }
            },
            "faqs_node": {
                "message": "الأسئلة الشائعة:\nس: ما هي مدة تنفيذ المشروع؟\nج: يتم التنفيذ خلال 3 إلى 4 أيام عمل.\nس: هل البوت يعمل بقواعد محددة؟\nج: نعم، يعتمد على سيناريو ثابت ومحدد بنسبة 100%.",
                "buttons": {
                    "1": {"text": "العودة للقائمة الرئيسية", "next_node": "start_node"},
                    "2": {"text": "إنهاء المحادثة", "next_node": "exit_node"}
                }
            },
            "contact_node": {
                "message": "يمكنك التواصل المباشر معنا عبر الوسائل التالية:\nالبريد الإلكتروني: support@nexura.com\nواتساب / الهاتف: 01060226375",
                "buttons": {
                    "1": {"text": "العودة للقائمة الرئيسية", "next_node": "start_node"}
                }
            },
            "exit_node": {
                "message": "شكراً لتواصلك مع Nexura Solutions! نتمنى لك يوماً سعيداً. 👋\n(اضغط 1 لإعادة بدء المحادثة)",
                "buttons": {
                    "1": {"text": "بدء محادثة جديدة", "next_node": "start_node"}
                }
            }
        }
        self.user_sessions = {}

    def get_user_session(self, user_id):
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = "start_node"
        return self.user_sessions[user_id]

    def set_user_session(self, user_id, node_id):
        self.user_sessions[user_id] = node_id

    def process_input(self, user_id, user_choice):
        if user_choice == "init_start":
            self.set_user_session(user_id, "start_node")
            return self.render_response("start_node")

        current_node_id = self.get_user_session(user_id)
        current_node = self.decision_tree.get(current_node_id)

        if user_choice in current_node.get("buttons", {}):
            next_node_id = current_node["buttons"][user_choice]["next_node"]
            self.set_user_session(user_id, next_node_id)
            return self.render_response(next_node_id)
        else:
            return self.render_error_response(current_node_id)

    def render_response(self, node_id):
        node = self.decision_tree[node_id]
        return {
            "message": node['message'],
            "buttons": node.get("buttons", {})
        }

    def render_error_response(self, current_node_id):
        node = self.decision_tree[current_node_id]
        return {
            "message": "⚠️ خيار غير صحيح! يرجى اختيار أحد الأرقام الموضحة من القائمة.",
            "buttons": node.get("buttons", {})
        }

bot_instance = RuleBasedChatbot()

class ChatRequest(BaseModel):
    user_id: str
    choice: str

HTML_UI = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexura Chatbot</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .chat-container { width: 100%; max-width: 450px; background: #1e293b; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.4); display: flex; flex-direction: column; height: 90vh; max-height: 650px; overflow: hidden; }
        .chat-header { background: #2563eb; padding: 18px; text-align: center; font-weight: bold; font-size: 19px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 14px; }
        .message { padding: 12px 16px; border-radius: 10px; max-width: 85%; line-height: 1.5; white-space: pre-line; word-break: break-word; }
        .user { background: #2563eb; align-self: flex-end; border-bottom-left-radius: 2px; }
        .bot { background: #334155; align-self: flex-start; border-bottom-right-radius: 2px; }
        .buttons-container { display: flex; flex-direction: column; gap: 8px; margin-top: 10px; width: 100%; }
        .chat-btn { background: #3b82f6; color: white; border: none; padding: 10px 14px; border-radius: 8px; cursor: pointer; text-align: right; font-size: 14px; transition: background 0.2s ease; }
        .chat-btn:hover { background: #1d4ed8; }
        .chat-input { display: flex; border-top: 1px solid #334155; padding: 12px; background: #0f172a; gap: 8px; }
        .chat-input input { flex: 1; padding: 10px 14px; border: 1px solid #334155; border-radius: 8px; background: #1e293b; color: #fff; outline: none; font-size: 14px; }
        .chat-input input:focus { border-color: #3b82f6; }
        .chat-input button { background: #2563eb; color: white; border: none; padding: 10px 18px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: background 0.2s ease; }
        .chat-input button:hover { background: #1d4ed8; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">شات بوت Nexura 🤖</div>
        <div class="chat-messages" id="chatMessages"></div>
        <div class="chat-input">
            <input type="text" id="userInput" placeholder="اكتب رقم الخيار هنا..." onkeypress="if(event.key === 'Enter') sendChoice()">
            <button onclick="sendChoice()">إرسال</button>
        </div>
    </div>

    <script>
        const userId = "web_user_" + Math.floor(Math.random() * 1000);

        function appendMessage(text, sender, buttons = {}) {
            const chatMessages = document.getElementById('chatMessages');
            let msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender}`;
            msgDiv.innerText = text;
            chatMessages.appendChild(msgDiv);

            if (sender === 'bot' && Object.keys(buttons).length > 0) {
                let btnContainer = document.createElement('div');
                btnContainer.className = 'buttons-container';
                for (let key in buttons) {
                    let btn = document.createElement('button');
                    btn.className = 'chat-btn';
                    btn.innerText = `${key}: ${buttons[key].text}`;
                    btn.onclick = () => sendChoice(key);
                    btnContainer.appendChild(btn);
                }
                chatMessages.appendChild(btnContainer);
            }
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function sendChoice(choiceOverride = null) {
            const input = document.getElementById('userInput');
            const choice = choiceOverride !== null ? choiceOverride : input.value.trim();
            if (!choice) return;

            if (choiceOverride === null) {
                appendMessage(choice, 'user');
                input.value = '';
            } else if (choiceOverride !== "init_start") {
                appendMessage(`اخترت: ${choiceOverride}`, 'user');
            }

            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, choice: choice })
            })
            .then(res => res.json())
            .then(data => {
                appendMessage(data.message, 'bot', data.buttons);
            });
        }

        window.onload = () => {
            sendChoice("init_start");
        };
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_UI

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    response_data = bot_instance.process_input(request.user_id, request.choice)
    return response_data
