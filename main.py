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
                "message": "شكراً لتواصلك مع Nexura Solutions! نتمنى لك يوماً سعيداً. 👋",
                "buttons": {}
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

# إنشاء كائن البوت
bot_instance = RuleBasedChatbot()

class ChatRequest(BaseModel):
    user_id: str
    choice: str

# واجهة الويب التفاعلية (HTML & CSS & JS) لتجربة البوت مباشرة من المتصفح
HTML_UI = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Nexura Chatbot</title>
    <style>
        body { font-family: Tahoma, sans-serif; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .chat-container { width: 450px; background: #1e293b; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); display: flex; flex-direction: column; overflow: hidden; height: 600px; }
        .chat-header { background: #3b82f6; padding: 15px; text-align: center; font-weight: bold; font-size: 18px; }
        .chat-messages { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; }
        .message { padding: 12px 16px; border-radius: 8px; max-width: 85%; line-height: 1.5; white-space: pre-line; }
        .user { background: #2563eb; align-self: flex-end; }
        .bot { background: #334155; align-self: flex-start; }
        .buttons-container { display: flex; flex-direction: column; gap: 6px; margin-top: 8px; }
        .chat-btn { background: #1d4ed8; color: white; border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer; text-align: right; font-size: 14px; }
        .chat-btn:hover { background: #2563eb; }
        .chat-input { display: flex; border-top: 1px solid #334155; padding: 10px; background: #0f172a; }
        .chat-input input { flex: 1; padding: 10px; border: none; border-radius: 6px; background: #1e293b; color: #fff; outline: none; }
        .chat-input button { background: #3b82f6; color: white; border: none; padding: 10px 15px; margin-right: 8px; border-radius: 6px; cursor: pointer; }
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
            } else {
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

        // بدء المحادثة تلقائياً عند فتح الصفحة
        window.onload = () => {
            sendChoice("1"); // أو البدء برقم البداية الافتراضي
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
