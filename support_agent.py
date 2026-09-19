import re
import sqlite3

import faiss
from sentence_transformers import SentenceTransformer


# ============================================================
# PATHS
# ============================================================

DATABASE_PATH = "data/database/orders.db"

INDEX_PATH = "data/index/company_policy.index"

CHUNKS_PATH = "data/index/chunks.txt"


# ============================================================
# LOAD AI KNOWLEDGE BASE
# ============================================================

print("Loading AI support system...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

index = faiss.read_index(
    INDEX_PATH
)

with open(
    CHUNKS_PATH,
    "r",
    encoding="utf-8"
) as file:

    chunks = file.read().split(
        "\n---CHUNK---\n"
    )

print("Knowledge base loaded.")


# ============================================================
# ORDER DATABASE
# ============================================================

def get_order(order_id):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            order_id,
            customer_name,
            product_name,
            order_status,
            order_date,
            expected_delivery,
            tracking_number
        FROM orders
        WHERE order_id = ?
        """,
        (order_id,)
    )

    order = cursor.fetchone()

    connection.close()

    return order


# ============================================================
# CREATE SUPPORT TICKET
# ============================================================

def create_ticket(
    issue,
    customer_name="Unknown",
    order_id=None,
    priority="Medium"
):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO support_tickets (
            customer_name,
            order_id,
            issue,
            priority,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            customer_name,
            order_id,
            issue,
            priority,
            "Open"
        )
    )

    ticket_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return ticket_id


# ============================================================
# EXTRACT ORDER ID
# ============================================================

def extract_order_id(question):

    match = re.search(
        r"\bORD\d+\b",
        question.upper()
    )

    if match:

        return match.group(0)

    return None


# ============================================================
# ORDER QUESTION DETECTION
# ============================================================

def is_order_question(question):

    question_lower = (
        question.lower()
    )

    # If an order number exists,
    # definitely treat it as an order query.

    if extract_order_id(question):

        return True


    order_lookup_keywords = [

        "order status",
        "tracking number",
        "tracking information",
        "track my order",
        "track order",
        "where is my order",
        "where is my package",
        "where is my parcel",
        "when will my order arrive",
        "when will my package arrive",
        "when will my parcel arrive",
        "has my order shipped",
        "is my order shipped",
        "order tracking",
        "track my package",
        "track my parcel"

    ]

    return any(
        keyword in question_lower
        for keyword in order_lookup_keywords
    )


# ============================================================
# HUMAN ESCALATION DETECTION
# ============================================================

def needs_human_escalation(question):

    question_lower = (
        question.lower()
        .strip()
    )


    # --------------------------------------------------------
    # REFUND NOT RECEIVED
    # --------------------------------------------------------

    refund_issue_phrases = [

        "my refund hasn't",
        "my refund has not",
        "refund hasn't arrived",
        "refund has not arrived",
        "refund not received",
        "refund not arrived",
        "i haven't received my refund",
        "i have not received my refund",
        "i didn't receive my refund",
        "i did not receive my refund",
        "my money hasn't",
        "my money has not",
        "money not received",
        "refund is missing",
        "refund still hasn't",
        "refund still has not"

    ]

    if any(
        phrase in question_lower
        for phrase in refund_issue_phrases
    ):

        return True


    # --------------------------------------------------------
    # HUMAN AGENT REQUEST
    # --------------------------------------------------------

    human_request_phrases = [

        "i want to speak to a human",
        "i want a human agent",
        "connect me to a human",
        "talk to a human",
        "speak to a human",
        "speak to an agent",
        "speak with an agent",
        "talk to an agent",
        "connect me to an agent",
        "human support",
        "human representative",
        "real person",
        "real agent",
        "customer service agent"

    ]

    if any(
        phrase in question_lower
        for phrase in human_request_phrases
    ):

        return True


    # --------------------------------------------------------
    # COMPLAINT REQUEST
    # --------------------------------------------------------

    complaint_phrases = [

        "file a complaint",
        "make a complaint",
        "raise a complaint",
        "i want to complain",
        "i want to raise a complaint"

    ]

    if any(
        phrase in question_lower
        for phrase in complaint_phrases
    ):

        return True


    # --------------------------------------------------------
    # DAMAGED / BROKEN PRODUCT COMPLAINTS
    # --------------------------------------------------------

    damaged_complaint_phrases = [

        "i received a damaged",
        "i received damaged",
        "received a damaged product",
        "received a damaged item",
        "received a damaged order",
        "received a broken product",
        "received a broken item",
        "received a broken order",

        "my product is damaged",
        "my item is damaged",
        "my order is damaged",

        "my product arrived damaged",
        "my item arrived damaged",
        "my order arrived damaged",

        "product arrived damaged",
        "item arrived damaged",
        "order arrived damaged",

        "my product is broken",
        "my item is broken",
        "my order is broken",

        "my product arrived broken",
        "my item arrived broken",
        "my order arrived broken",

        "product arrived broken",
        "item arrived broken",
        "order arrived broken",

        "package arrived damaged",
        "package arrived broken",
        "parcel arrived damaged",
        "parcel arrived broken",

        "my package is damaged",
        "my package is broken",
        "my parcel is damaged",
        "my parcel is broken"

    ]

    if any(
        phrase in question_lower
        for phrase in damaged_complaint_phrases
    ):

        return True


    return False


# ============================================================
# RAG POLICY RETRIEVAL
# ============================================================

def retrieve_policy(question):

    query_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")


    distances, indices = index.search(
        query_embedding,
        3
    )


    valid_chunks = []

    for i in indices[0]:

        if 0 <= i < len(chunks):

            valid_chunks.append(
                chunks[i]
            )


    retrieved_context = "\n\n".join(
        valid_chunks
    )


    return retrieved_context