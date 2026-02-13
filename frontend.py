import streamlit as st
from ai_researcher2 import INITIAL_PROMPT, graph, config
from pathlib import Path
import logging
from langchain_core.messages import AIMessage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------------------
# ADDITION: clean AI message content
# ----------------------------------------
def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            part.get("text", "") for part in content if isinstance(part, dict)
        )
    return str(content)

# Basic app config
st.set_page_config(page_title="Research AI Agent", page_icon="📄")
st.title("📄 Research AI Agent")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.info("Initialized chat history")

# ----------------------------------------
# ADDITION: store generated PDF path
# ----------------------------------------
if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

# ----------------------------------------
# Render previous conversation
# ----------------------------------------
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])



# Chat interface
user_input = st.chat_input("What research topic would you like to explore?")

if user_input:
    # Log and display user input
    logger.info(f"User input: {user_input}")
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Prepare input for the agent
    chat_input = {
        "messages": [{"role": "system", "content": INITIAL_PROMPT}]
        + st.session_state.chat_history
    }
    logger.info("Starting agent processing...")

    # Stream agent response
    full_response = ""
    assistant_placeholder = st.chat_message("assistant")

    for s in graph.stream(chat_input, config, stream_mode="values"):
        message = s["messages"][-1]

        # Handle tool calls (log only, no UI noise)
        if getattr(message, "tool_calls", None):
            for tool_call in message.tool_calls:
                logger.info(f"Tool call: {tool_call['name']}")
            continue

        # Handle assistant response (clean)
        if isinstance(message, AIMessage) and message.content:
            text_content = extract_text(message.content)
            full_response = text_content
            assistant_placeholder.write(full_response)

            # ----------------------------------------
            # ADDITION: capture PDF path from tool output
            # ----------------------------------------
            # if (
            #     isinstance(text_content, str)
            #     and text_content.endswith(".pdf")
            #     and Path(text_content).exists()
            # ):
            #     st.session_state.pdf_path = text_content
            #     logger.info(f"PDF generated at: {text_content}")

            # ----------------------------------------
            # ADDITION: capture PDF path from tool output (ROBUST)
            # ----------------------------------------
            if isinstance(text_content, str):
                for token in text_content.split():
                    if token.endswith(".pdf") and Path(token).exists():
                        st.session_state.pdf_path = token
                        logger.info(f"PDF generated at: {token}")


    # Add final response to history
    if full_response:
        st.session_state.chat_history.append(
            {"role": "assistant", "content": full_response}
        )
# ----------------------------------------
# Show download button if PDF exists
# ----------------------------------------
if st.session_state.pdf_path and Path(st.session_state.pdf_path).exists():
    pdf_file = Path(st.session_state.pdf_path)
    with open(pdf_file, "rb") as f:
        st.download_button(
            label="⬇️ Download Generated Research Paper (PDF)",
            data=f,
            file_name=pdf_file.name,
            mime="application/pdf",
        )