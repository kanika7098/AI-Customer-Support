import sqlite3
from datetime import datetime

import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

DATABASE_PATH = "data/database/orders.db"

STATUS_OPTIONS = [
    "Open",
    "In Progress",
    "Closed"
]

PRIORITY_OPTIONS = [
    "All",
    "High",
    "Medium"
]


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Support Command Center",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main application */

    .stApp {
        background-color: #f5f7fb;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }


    /* Header */

    .dashboard-header {
        background: white;
        padding: 1.5rem 1.8rem;
        border-radius: 16px;
        border: 1px solid #e4e7ec;
        margin-bottom: 1.5rem;
    }

    .dashboard-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 750;
    }

    .dashboard-header p {
        margin-top: 0.4rem;
        color: #667085;
        font-size: 1rem;
    }


    /* Metric cards */

    .metric-card {
        background: white;
        border: 1px solid #e4e7ec;
        border-radius: 14px;
        padding: 1.2rem;
        min-height: 115px;
    }

    .metric-title {
        color: #667085;
        font-size: 0.9rem;
        font-weight: 600;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 750;
        margin-top: 0.3rem;
    }


    /* Ticket cards */

    .ticket-card {
        background: white;
        border: 1px solid #e4e7ec;
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
    }


    /* Section titles */

    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }


    /* Sidebar */

    [data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e4e7ec;
    }


    /* Buttons */

    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 40px;
    }


    /* Tables */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
    }


    /* Alerts */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* Expanders */

    [data-testid="stExpander"] {
        background: white;
        border: 1px solid #e4e7ec;
        border-radius: 12px;
        margin-bottom: 0.6rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return sqlite3.connect(
        DATABASE_PATH
    )


# ============================================================
# GET TICKET STATISTICS
# ============================================================

def get_statistics():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM support_tickets
        """
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM support_tickets
        WHERE status = 'Open'
        """
    )

    open_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM support_tickets
        WHERE status = 'In Progress'
        """
    )

    progress_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM support_tickets
        WHERE status = 'Closed'
        """
    )

    closed_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM support_tickets
        WHERE priority = 'High'
        """
    )

    high_priority = cursor.fetchone()[0]

    connection.close()

    return {
        "total": total,
        "open": open_count,
        "progress": progress_count,
        "closed": closed_count,
        "high": high_priority
    }


# ============================================================
# GET ALL TICKETS
# ============================================================

def get_tickets():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            ticket_id,
            customer_name,
            order_id,
            issue,
            priority,
            status,
            created_at
        FROM support_tickets
        ORDER BY ticket_id DESC
        """
    )

    tickets = cursor.fetchall()

    connection.close()

    return tickets


# ============================================================
# UPDATE TICKET STATUS
# ============================================================

def update_ticket_status(
    ticket_id,
    new_status
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE support_tickets
        SET status = ?
        WHERE ticket_id = ?
        """,
        (
            new_status,
            ticket_id
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# DELETE TICKET
# ============================================================

def delete_ticket(ticket_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM support_tickets
        WHERE ticket_id = ?
        """,
        (ticket_id,)
    )

    connection.commit()

    connection.close()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🎧 Support Center"
    )

    st.caption(
        "AI Customer Support Command Center"
    )

    st.divider()

    st.markdown(
        "### Navigation"
    )

    page = st.radio(
        "Go to",
        [
            "📊 Overview",
            "🎫 Ticket Management",
            "📈 Analytics"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(
        "### System Status"
    )

    st.success(
        "AI Support: Online"
    )

    st.success(
        "Knowledge Base: Online"
    )

    st.success(
        "Order Database: Online"
    )

    st.success(
        "Ticket System: Online"
    )

    st.divider()

    if st.button(
        "🔄 Refresh Dashboard",
        use_container_width=True
    ):

        st.rerun()


# ============================================================
# LOAD DATA
# ============================================================

statistics = get_statistics()

tickets = get_tickets()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="dashboard-header">

        <h1>🎧 AI Support Command Center</h1>

        <p>
            Monitor customer issues, manage support tickets,
            and track the performance of the AI customer-support system.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "📊 Overview":

    st.markdown(
        '<div class="section-title">System Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:

        st.metric(
            "Total Tickets",
            statistics["total"]
        )


    with col2:

        st.metric(
            "Open",
            statistics["open"]
        )


    with col3:

        st.metric(
            "In Progress",
            statistics["progress"]
        )


    with col4:

        st.metric(
            "Closed",
            statistics["closed"]
        )


    with col5:

        st.metric(
            "High Priority",
            statistics["high"]
        )


    st.divider()


    # --------------------------------------------------------
    # RECENT TICKETS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🕐 Recent Support Tickets</div>',
        unsafe_allow_html=True
    )


    recent_tickets = tickets[:5]


    if not recent_tickets:

        st.info(
            "No support tickets have been created yet."
        )

    else:

        for ticket in recent_tickets:

            (
                ticket_id,
                customer_name,
                order_id,
                issue,
                priority,
                status,
                created_at
            ) = ticket


            with st.expander(
                f"Ticket #{ticket_id}  •  "
                f"{priority} Priority  •  "
                f"{status}"
            ):

                col1, col2 = st.columns(2)


                with col1:

                    st.write(
                        f"**Customer:** {customer_name}"
                    )

                    st.write(
                        f"**Order ID:** "
                        f"{order_id if order_id else 'None'}"
                    )


                with col2:

                    st.write(
                        f"**Priority:** {priority}"
                    )

                    st.write(
                        f"**Created:** {created_at}"
                    )


                st.write(
                    "**Customer Issue:**"
                )

                st.info(issue)


    st.divider()


    # --------------------------------------------------------
    # PRIORITY SUMMARY
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🚨 Priority Summary</div>',
        unsafe_allow_html=True
    )


    high_count = statistics["high"]

    medium_count = (
        statistics["total"]
        - high_count
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "🔴 High Priority",
            high_count
        )


    with col2:

        st.metric(
            "🟡 Medium Priority",
            medium_count
        )


# ============================================================
# TICKET MANAGEMENT PAGE
# ============================================================

elif page == "🎫 Ticket Management":

    st.markdown(
        '<div class="section-title">🎫 Ticket Management</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    filter_col1, filter_col2, filter_col3 = st.columns(
        [2, 2, 3]
    )


    with filter_col1:

        status_filter = st.selectbox(
            "Status",
            [
                "All",
                "Open",
                "In Progress",
                "Closed"
            ]
        )


    with filter_col2:

        priority_filter = st.selectbox(
            "Priority",
            PRIORITY_OPTIONS
        )


    with filter_col3:

        search_text = st.text_input(
            "Search",
            placeholder="Ticket ID, Order ID, customer, or issue..."
        )


    # --------------------------------------------------------
    # FILTER DATA
    # --------------------------------------------------------

    filtered_tickets = []


    for ticket in tickets:

        (
            ticket_id,
            customer_name,
            order_id,
            issue,
            priority,
            status,
            created_at
        ) = ticket


        # Status filter

        if (
            status_filter != "All"
            and status != status_filter
        ):

            continue


        # Priority filter

        if (
            priority_filter != "All"
            and priority != priority_filter
        ):

            continue


        # Search filter

        if search_text:

            search_lower = search_text.lower()

            searchable_text = " ".join(
                [
                    str(ticket_id),
                    str(customer_name),
                    str(order_id),
                    str(issue),
                    str(priority),
                    str(status)
                ]
            ).lower()


            if search_lower not in searchable_text:

                continue


        filtered_tickets.append(ticket)


    # --------------------------------------------------------
    # RESULTS COUNT
    # --------------------------------------------------------

    st.caption(
        f"Showing {len(filtered_tickets)} "
        f"of {len(tickets)} tickets"
    )


    # --------------------------------------------------------
    # TICKET TABLE
    # --------------------------------------------------------

    if filtered_tickets:

        table_data = []


        for ticket in filtered_tickets:

            (
                ticket_id,
                customer_name,
                order_id,
                issue,
                priority,
                status,
                created_at
            ) = ticket


            table_data.append(
                {
                    "Ticket": f"#{ticket_id}",
                    "Customer": customer_name,
                    "Order": (
                        order_id
                        if order_id
                        else "-"
                    ),
                    "Priority": priority,
                    "Status": status,
                    "Created": created_at
                }
            )


        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )


        st.divider()


        # ----------------------------------------------------
        # TICKET DETAILS
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">Ticket Details</div>',
            unsafe_allow_html=True
        )


        ticket_ids = [
            ticket[0]
            for ticket in filtered_tickets
        ]


        selected_ticket_id = st.selectbox(
            "Select Ticket",
            ticket_ids,
            format_func=lambda x: f"Ticket #{x}"
        )


        selected_ticket = next(
            ticket
            for ticket in filtered_tickets
            if ticket[0] == selected_ticket_id
        )


        (
            ticket_id,
            customer_name,
            order_id,
            issue,
            priority,
            status,
            created_at
        ) = selected_ticket


        detail_col1, detail_col2 = st.columns(2)


        with detail_col1:

            st.write(
                f"**Ticket ID:** #{ticket_id}"
            )

            st.write(
                f"**Customer:** {customer_name}"
            )

            st.write(
                f"**Order ID:** "
                f"{order_id if order_id else 'None'}"
            )


        with detail_col2:

            st.write(
                f"**Priority:** {priority}"
            )

            st.write(
                f"**Current Status:** {status}"
            )

            st.write(
                f"**Created:** {created_at}"
            )


        st.write(
            "**Customer Issue:**"
        )

        st.info(issue)


        # ----------------------------------------------------
        # STATUS UPDATE
        # ----------------------------------------------------

        update_col1, update_col2 = st.columns(
            [3, 1]
        )


        with update_col1:

            current_index = (
                STATUS_OPTIONS.index(status)
                if status in STATUS_OPTIONS
                else 0
            )


            new_status = st.selectbox(
                "Change Status",
                STATUS_OPTIONS,
                index=current_index,
                key=f"new_status_{ticket_id}"
            )


        with update_col2:

            st.write("")


            if st.button(
                "Update Status",
                use_container_width=True
            ):

                update_ticket_status(
                    ticket_id,
                    new_status
                )

                st.success(
                    f"Ticket #{ticket_id} is now "
                    f"{new_status}."
                )

                st.rerun()


        # ----------------------------------------------------
        # DANGER ZONE
        # ----------------------------------------------------

        st.divider()

        with st.expander(
            "⚠️ Advanced Actions"
        ):

            st.warning(
                "Deleting a ticket permanently removes "
                "it from the database."
            )


            if st.button(
                "Delete Ticket",
                type="secondary"
            ):

                delete_ticket(
                    ticket_id
                )

                st.success(
                    f"Ticket #{ticket_id} deleted."
                )

                st.rerun()


    else:

        st.info(
            "No tickets match the selected filters."
        )


# ============================================================
# ANALYTICS PAGE
# ============================================================

elif page == "📈 Analytics":

    st.markdown(
        '<div class="section-title">📈 Support Analytics</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # STATUS DISTRIBUTION
    # --------------------------------------------------------

    status_counts = {
        "Open": 0,
        "In Progress": 0,
        "Closed": 0
    }


    for ticket in tickets:

        status = ticket[5]

        if status in status_counts:

            status_counts[status] += 1


    st.subheader(
        "Ticket Status Distribution"
    )


    status_chart_data = {
        "Status": [
            "Open",
            "In Progress",
            "Closed"
        ],
        "Tickets": [
            status_counts["Open"],
            status_counts["In Progress"],
            status_counts["Closed"]
        ]
    }


    st.bar_chart(
        status_chart_data,
        x="Status",
        y="Tickets"
    )


    st.divider()


    # --------------------------------------------------------
    # PRIORITY DISTRIBUTION
    # --------------------------------------------------------

    priority_counts = {
        "High": 0,
        "Medium": 0
    }


    for ticket in tickets:

        priority = ticket[4]

        if priority in priority_counts:

            priority_counts[priority] += 1


    st.subheader(
        "Ticket Priority Distribution"
    )


    priority_chart_data = {
        "Priority": [
            "High",
            "Medium"
        ],
        "Tickets": [
            priority_counts["High"],
            priority_counts["Medium"]
        ]
    }


    st.bar_chart(
        priority_chart_data,
        x="Priority",
        y="Tickets"
    )


    st.divider()


    # --------------------------------------------------------
    # TICKET SUMMARY
    # --------------------------------------------------------

    st.subheader(
        "Support Summary"
    )


    summary_col1, summary_col2, summary_col3 = st.columns(3)


    with summary_col1:

        st.metric(
            "Total Conversations Escalated",
            statistics["total"]
        )


    with summary_col2:

        st.metric(
            "Currently Active",
            statistics["open"]
            + statistics["progress"]
        )


    with summary_col3:

        if statistics["total"] > 0:

            resolution_rate = (
                statistics["closed"]
                / statistics["total"]
            ) * 100

        else:

            resolution_rate = 0


        st.metric(
            "Closed Ticket Rate",
            f"{resolution_rate:.1f}%"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Customer Support System • "
    "Powered by local AI, RAG, SQLite and Streamlit"
)