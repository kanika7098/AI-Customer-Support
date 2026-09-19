import re

import streamlit as st
from ollama import chat

from support_agent import (
    get_order,
    extract_order_id,
    is_order_question,
    needs_human_escalation,
    retrieve_policy
)

from ticket_manager import create_ticket


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM UI STYLING
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f7fb;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e4e7ec;
    }

    [data-testid="stChatMessage"] {
        border-radius: 14px;
        margin-bottom: 10px;
        padding: 12px 16px;
    }

    [data-testid="stChatInput"] {
        border-radius: 14px;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }

    [data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e4e7ec;
        border-radius: 12px;
        padding: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_question" not in st.session_state:
    st.session_state.quick_question = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 AI Support")

    st.caption(
        "E-Commerce Customer Support"
    )

    st.divider()

    st.subheader("System Status")

    st.success(
        "🤖 AI Assistant: Online"
    )

    st.success(
        "📚 Knowledge Base: Online"
    )

    st.success(
        "📦 Order System: Online"
    )

    st.success(
        "🎫 Ticket System: Online"
    )

    st.divider()

    st.subheader(
        "What I can help with"
    )

    st.write("📦 Order tracking")
    st.write("🔄 Returns")
    st.write("💰 Refunds")
    st.write("🚚 Delivery")
    st.write("❌ Order cancellation")
    st.write("🎫 Support escalation")

    st.divider()

    if st.button(
        "🧹 Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption(
        "Powered by local AI"
    )

    st.caption(
        "Ollama • Qwen2.5 • RAG • FAISS • SQLite"
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.title(
    "🤖 AI Customer Support"
)

st.write(
    "Get instant help with orders, returns, refunds, "
    "delivery, cancellations, and other "
    "e-commerce support questions."
)


# ============================================================
# SYSTEM STATUS
# ============================================================

st.subheader(
    "System Status"
)

status1, status2, status3 = st.columns(3)

with status1:

    st.metric(
        "🤖 AI Assistant",
        "Online"
    )

with status2:

    st.metric(
        "📚 Company Knowledge",
        "Connected"
    )

with status3:

    st.metric(
        "📦 Order Database",
        "Connected"
    )


# ============================================================
# QUICK HELP
# ============================================================

st.divider()

st.subheader(
    "⚡ Quick Help"
)

quick1, quick2, quick3, quick4 = st.columns(4)


with quick1:

    st.write(
        "### 📦 Track Order"
    )

    st.caption(
        "Check order status and tracking information."
    )

    if st.button(
        "Track an Order",
        use_container_width=True
    ):

        st.session_state.quick_question = (
            "Where is my order?"
        )

        st.rerun()


with quick2:

    st.write(
        "### 🔄 Returns"
    )

    st.caption(
        "Learn about our return policy."
    )

    if st.button(
        "Return Policy",
        use_container_width=True
    ):

        st.session_state.quick_question = (
            "What is your return policy?"
        )

        st.rerun()


with quick3:

    st.write(
        "### 💰 Refunds"
    )

    st.caption(
        "Learn how refunds are processed."
    )

    if st.button(
        "Refund Policy",
        use_container_width=True
    ):

        st.session_state.quick_question = (
            "What is your refund policy?"
        )

        st.rerun()


with quick4:

    st.write(
        "### 🚚 Delivery"
    )

    st.caption(
        "Learn about delivery times."
    )

    if st.button(
        "Delivery Policy",
        use_container_width=True
    ):

        st.session_state.quick_question = (
            "How long does delivery take?"
        )

        st.rerun()


# ============================================================
# SUPPORT CHAT
# ============================================================

st.divider()

st.subheader(
    "💬 Support Chat"
)


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# POLICY QUESTION HANDLER
# ============================================================

def get_policy_answer(question):

    question_lower = (
        question.lower().strip()
    )


    # --------------------------------------------------------
    # RETURN POLICY
    # --------------------------------------------------------

    return_keywords = [

        "return policy",
        "return an item",
        "return my item",
        "return product",
        "return a product",
        "can i return",
        "eligible for return",
        "return eligibility",
        "how do returns work",
        "how can i return",
        "want to return"
    ]


    if any(
        keyword in question_lower
        for keyword in return_keywords
    ):

        return (

            "According to our company policy, eligible "
            "products can be returned within **30 days "
            "of delivery**.\n\n"

            "The product must be **unused** and returned "
            "in its **original packaging**.\n\n"

            "Some products may not be eligible for return, "
            "including **personalized products** and certain "
            "**hygiene-related products**."
        )


    # --------------------------------------------------------
    # RETURN PERIOD QUESTIONS
    # --------------------------------------------------------

    if (
        "return" in question_lower
        and (
            "day" in question_lower
            or "days" in question_lower
        )
    ):

        day_match = re.search(
            r"(\d+)\s*days?",
            question_lower
        )


        if day_match:

            days = int(
                day_match.group(1)
            )


            if days <= 30:

                return (

                    "Yes. According to our company policy, "
                    "eligible products can be returned within "
                    "**30 days of delivery**.\n\n"

                    f"The **{days}-day** period mentioned "
                    "in your question is within that "
                    "30-day return window.\n\n"

                    "The product must be unused and returned "
                    "in its original packaging."
                )


            return (

                "According to our company policy, eligible "
                "products can be returned within **30 days "
                "of delivery**.\n\n"

                f"**{days} days** is beyond the standard "
                "30-day return period."
            )


    # --------------------------------------------------------
    # REFUND POLICY
    # --------------------------------------------------------

    refund_policy_keywords = [

        "refund policy",
        "how do refunds work",
        "how is refund",
        "when is refund",
        "refund process",
        "refund processed",
        "refund processing",
        "how long does refund",
        "how long will refund",
        "when will i get my refund"
    ]


    if any(
        keyword in question_lower
        for keyword in refund_policy_keywords
    ):

        return (

            "According to our company policy, after a "
            "returned product is **inspected and approved**, "
            "the refund is initiated.\n\n"

            "Refunds are normally processed within "
            "**5–7 business days**.\n\n"

            "The actual time for the money to appear in "
            "your account may depend on your payment provider."
        )


    # --------------------------------------------------------
    # DELIVERY POLICY
    # --------------------------------------------------------

    delivery_keywords = [

        "delivery policy",
        "how long does delivery",
        "how long will delivery",
        "delivery time",
        "delivery take",
        "when will my package arrive",
        "when will my order arrive",
        "shipping time",
        "shipping take"
    ]


    if any(
        keyword in question_lower
        for keyword in delivery_keywords
    ):

        return (

            "According to our company policy, standard "
            "delivery usually takes **3–7 business days "
            "after shipment**.\n\n"

            "Delivery times can vary depending on location, "
            "courier delays, weather, and other circumstances.\n\n"

            "If an order is significantly delayed, please "
            "contact customer support with your order number."
        )


    # --------------------------------------------------------
    # ORDER CANCELLATION
    # --------------------------------------------------------

    cancellation_keywords = [

        "cancel my order",
        "cancel an order",
        "cancel order",
        "order cancellation",
        "cancellation policy",
        "can i cancel",
        "want to cancel",
        "how do i cancel"
    ]


    if any(
        keyword in question_lower
        for keyword in cancellation_keywords
    ):

        return (

            "According to our company policy, customers can "
            "request cancellation **before an order is shipped**.\n\n"

            "Once an order has been shipped, cancellation "
            "**may no longer be possible**.\n\n"

            "In that situation, the customer may instead need "
            "to use the return process after delivery."
        )


    # --------------------------------------------------------
    # DAMAGED PRODUCT POLICY
    # --------------------------------------------------------

    damaged_policy_questions = [

        "damaged product policy",
        "damaged item policy",
        "damaged order policy",

        "what if my product is damaged",
        "what if my item is damaged",
        "what if my order is damaged",

        "what should i do if my product is damaged",
        "what should i do if my item is damaged",
        "what should i do if my order is damaged",

        "what if my item is broken",
        "what if my product is broken",
        "what if my order is broken",

        "what should i do if my item is broken",
        "what should i do if my product is broken",
        "what should i do if my order is broken",

        "what do i do if my product is damaged",
        "what do i do if my item is damaged",
        "what do i do if my order is damaged",

        "what do i do if my product is broken",
        "what do i do if my item is broken",
        "what do i do if my order is broken"
    ]


    if any(
        keyword in question_lower
        for keyword in damaged_policy_questions
    ):

        return (

            "According to our company policy, customers "
            "who receive a damaged product should contact "
            "customer support as soon as possible.\n\n"

            "You may be asked to provide photographs of "
            "the damaged product and its packaging.\n\n"

            "The support team will review the case and "
            "determine the appropriate resolution."
        )


    return None


# ============================================================
# UNSUPPORTED POLICY QUESTION DETECTION
# ============================================================

def is_unsupported_policy_question(question):

    question_lower = (
        question.lower().strip()
    )


    # --------------------------------------------------------
    # COMPENSATION
    # --------------------------------------------------------

    compensation_keywords = [

        "compensation",
        "compensate me",
        "compensate",
        "get compensation",
        "receive compensation"
    ]


    if any(
        keyword in question_lower
        for keyword in compensation_keywords
    ):

        return True


    # --------------------------------------------------------
    # DISCOUNT
    # --------------------------------------------------------

    discount_keywords = [

        "discount",
        "give me a discount",
        "get a discount",
        "coupon",
        "voucher",
        "promo code"
    ]


    if any(
        keyword in question_lower
        for keyword in discount_keywords
    ):

        return True


    # --------------------------------------------------------
    # GUARANTEE
    # --------------------------------------------------------

    guarantee_keywords = [

        "guarantee",
        "guaranteed",
        "guarantee delivery",
        "guaranteed delivery",
        "guarantee a refund",
        "guaranteed refund"
    ]


    if any(
        keyword in question_lower
        for keyword in guarantee_keywords
    ):

        return True


    # --------------------------------------------------------
    # DELAY + REFUND
    # --------------------------------------------------------

    delay_keywords = [

        "delayed",
        "delay",
        "late delivery",
        "delivery is late",
        "order is late",
        "package is late"
    ]


    refund_keywords = [

        "refund",
        "money back",
        "moneyback"
    ]


    if (
        any(
            keyword in question_lower
            for keyword in delay_keywords
        )
        and
        any(
            keyword in question_lower
            for keyword in refund_keywords
        )
    ):

        return True


    return False


# ============================================================
# DAMAGED POLICY QUESTION CHECK
# ============================================================

def is_damaged_policy_question(question):

    question_lower = (
        question.lower().strip()
    )


    policy_question_phrases = [

        "what if my product is damaged",
        "what if my item is damaged",
        "what if my order is damaged",

        "what should i do if my product is damaged",
        "what should i do if my item is damaged",
        "what should i do if my order is damaged",

        "what if my product is broken",
        "what if my item is broken",
        "what if my order is broken",

        "what should i do if my product is broken",
        "what should i do if my item is broken",
        "what should i do if my order is broken",

        "what do i do if my product is damaged",
        "what do i do if my item is damaged",
        "what do i do if my order is damaged",

        "what do i do if my product is broken",
        "what do i do if my item is broken",
        "what do i do if my order is broken"
    ]


    return any(
        phrase in question_lower
        for phrase in policy_question_phrases
    )


# ============================================================
# GET CUSTOMER QUESTION
# ============================================================

question = None


if st.session_state.quick_question:

    question = (
        st.session_state.quick_question
    )

    st.session_state.quick_question = None


chat_question = st.chat_input(
    "Ask your support question..."
)


if chat_question:

    question = chat_question


# ============================================================
# PROCESS CUSTOMER QUESTION
# ============================================================

if question:

    # --------------------------------------------------------
    # DISPLAY USER MESSAGE
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(
            question
        )


    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    answer = None


    # ========================================================
    # 1. POLICY QUESTION ABOUT DAMAGED PRODUCT
    # ========================================================
    #
    # IMPORTANT:
    # This must happen BEFORE human escalation.
    #
    # Example:
    # "What should I do if my product is damaged?"
    #
    # should explain policy, not create a ticket.
    # ========================================================

    if is_damaged_policy_question(
        question
    ):

        answer = get_policy_answer(
            question
        )


    # ========================================================
    # 2. HUMAN ESCALATION
    # ========================================================

    elif needs_human_escalation(
        question
    ):

        order_id = extract_order_id(
            question
        )


        ticket_id = create_ticket(
            issue=question,
            customer_name="Customer",
            order_id=order_id,
            priority="High"
        )


        answer = (

            "I'm sorry you're experiencing this issue. "
            "This situation needs to be reviewed by a "
            "human support agent.\n\n"

            f"I have created support ticket **#{ticket_id}** "
            "for you.\n\n"

            "A support agent can review the issue and "
            "assist you further."
        )


    # ========================================================
    # 3. UNSUPPORTED POLICY QUESTION
    # ========================================================

    elif is_unsupported_policy_question(
        question
    ):

        answer = (

            "Our available company policy does not specify "
            "whether this type of compensation, discount, "
            "refund, or guarantee is available.\n\n"

            "If your order is affected by an issue, please "
            "contact customer support with your order number "
            "so a support agent can review your situation."
        )


    # ========================================================
    # 4. ORDER QUESTION
    # ========================================================

    elif is_order_question(
        question
    ):

        order_id = extract_order_id(
            question
        )


        # ----------------------------------------------------
        # ORDER ID PROVIDED
        # ----------------------------------------------------

        if order_id:

            order = get_order(
                order_id
            )


            # ------------------------------------------------
            # ORDER FOUND
            # ------------------------------------------------

            if order:

                answer = (

                    f"### 📦 Order {order[0]}\n\n"

                    f"**Product:** {order[2]}\n\n"

                    f"**Current status:** {order[3]}\n\n"

                    f"**Expected delivery:** {order[5]}\n\n"
                )


                if order[6]:

                    answer += (

                        f"**Tracking number:** "
                        f"{order[6]}"
                    )


                else:

                    answer += (

                        "Tracking information is not "
                        "available for this order yet."
                    )


            # ------------------------------------------------
            # ORDER NOT FOUND
            # ------------------------------------------------

            else:

                ticket_id = create_ticket(
                    issue=question,
                    customer_name="Customer",
                    order_id=order_id,
                    priority="Medium"
                )


                answer = (

                    f"I couldn't find order "
                    f"**{order_id}** in our system.\n\n"

                    f"I have created support ticket "
                    f"**#{ticket_id}** so a human support "
                    "agent can investigate this."
                )


        # ----------------------------------------------------
        # NO ORDER ID
        # ----------------------------------------------------

        else:

            answer = (

                "I'd be happy to check your order. 📦\n\n"

                "Please provide your **order number**, "
                "for example `ORD1001`."
            )


    # ========================================================
    # 5. STANDARD POLICY QUESTION
    # ========================================================

    else:

        answer = get_policy_answer(
            question
        )


    # ========================================================
    # 6. RAG + LOCAL LLM FALLBACK
    # ========================================================

    if answer is None:

        context = retrieve_policy(
            question
        )


        prompt = f"""
You are a professional e-commerce customer support agent.

Answer the customer's question using ONLY the company
information provided below.

COMPANY INFORMATION:

{context}

CUSTOMER QUESTION:

{question}

STRICT RULES:

1. Never invent company policies.

2. Never invent order information.

3. Never invent tracking information.

4. Never invent refund status.

5. Never invent delivery status.

6. Never invent prices.

7. Never invent dates.

8. Never invent compensation.

9. Never invent discounts.

10. Never invent coupons.

11. Never invent guarantees.

12. Never invent benefits.

13. Never promise compensation unless the company
    information explicitly states that compensation
    is available.

14. Never promise a refund for a situation unless
    the company information explicitly supports it.

15. Never create exceptions that are not present
    in the company information.

16. Preserve words such as "may", "normally",
    and "usually".

17. Never change "may" into "will".

18. If the company information does not specify
    the requested information, clearly say that
    the available company policy does not specify it.

19. If an issue requires individual investigation,
    tell the customer to contact customer support
    with their order number.

20. Never guess.

21. Keep the response concise and professional.

22. Do not mention AI, LLM, RAG, FAISS, embeddings,
    prompts, databases, or internal implementation.

Answer only the customer's question.

FINAL ANSWER:
"""


        response = chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )


        answer = (
            response.message.content
            .strip()
        )


    # ========================================================
    # DISPLAY ASSISTANT RESPONSE
    # ========================================================

    with st.chat_message(
        "assistant"
    ):

        st.markdown(
            answer
        )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Customer Support System • "
    "Powered by local AI, RAG, FAISS, SQLite and Streamlit"
)