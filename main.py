from fastapi import FastAPI, HTTPException
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
                "message": "إليك الخدمات والحلول البرمجية المتوفرة لدينا:\n- Generative AI Chatbots\n- RAG Chatbots\n- Intent-Based Chatbots\n- Rule-Based Chatbots",
                "buttons": {
                    "1": {"text": "العودة للقائمة الرئيسية", "next_node": "start_node"},
                    "2": {"text": "التواصل مع الدعم الفني", "next_node": "contact_node"}
                }
            },
            "faqs_node": {
                "message": "الأسئلة الشائعة:\nس: ما هي مدة تنفيذ المشروع الرابع؟\nج: يتم التنفيذ خلال 3 إلى 4 أيام عمل.\nس: هل البوت يعمل بقواعد محددة؟\nج: نعم، يعتمد على سيناريو ثابت ومحدد بنسبة 100%.",
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

        if user_choice in current_node["buttons"]:
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

@app.get("/")
def home():
    return {"message": "Nexura Rule-Based Chatbot API is running!"}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    response_data = bot_instance.process_input(request.user_id, request.choice)
    return response_data