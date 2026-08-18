import streamlit as st

from utils.youtube import extract_video_id
from ingestion.youtube_vector_store import create_youtube_vector_store
from chains.rag_chain import generate_answer


st.set_page_config(
    page_title="YouTube RAG Chatbot",
    page_icon="🎥",
    layout="wide"
)


st.title("🎥 YouTube RAG Chatbot")
st.write(
    "Paste a YouTube video URL and ask questions about its content."
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "video_id" not in st.session_state:
    st.session_state.video_id = None

if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Controls")

    if st.button(
        "🆕 New Video",
        use_container_width=True
    ):

        st.session_state.video_id = None
        st.session_state.video_loaded = False
        st.session_state.messages = []

        st.rerun()


    if st.session_state.video_loaded:

        st.divider()

        st.write("**Current Video**")

        st.code(
            st.session_state.video_id
        )


# --------------------------------------------------
# YouTube URL
# --------------------------------------------------

youtube_url = st.text_input(
    "YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=..."
)


if st.button(
    "▶️ Load Video",
    use_container_width=True
):

    if not youtube_url.strip():

        st.warning(
            "Please enter a YouTube URL."
        )

    else:

        try:

            video_id = extract_video_id(
                youtube_url.strip()
            )

            if not video_id:

                st.error(
                    "Invalid YouTube URL."
                )

            else:

                with st.spinner(
                    "Loading video..."
                ):

                    create_youtube_vector_store(
                        video_id
                    )

                st.session_state.video_id = video_id
                st.session_state.video_loaded = True
                st.session_state.messages = []

                st.success(
                    "Video loaded successfully! "
                    "You can now ask questions."
                )

        except Exception as e:

            error_message = str(e)

            if "NoTranscriptFound" in error_message:

                st.error(
                    "❌ This video does not have "
                    "a transcript available."
                )

            elif "IpBlocked" in error_message:

                st.error(
                    "❌ YouTube temporarily blocked "
                    "the transcript request. "
                    "Please try again later."
                )

            elif "VideoUnavailable" in error_message:

                st.error(
                    "❌ This YouTube video is unavailable."
                )

            elif "HTTP" in error_message:

                st.error(
                    "❌ A network/API error occurred. "
                    "Please try again."
                )

            else:

                st.error(
                    f"❌ Could not load video: {error_message}"
                )


# --------------------------------------------------
# Chat
# --------------------------------------------------

if st.session_state.video_loaded:

    st.divider()

    st.subheader("💬 Chat with the Video")


    # ----------------------------------------------
    # Display conversation
    # ----------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # ----------------------------------------------
    # Chat input
    # ----------------------------------------------

    query = st.chat_input(
        "Ask something about the video..."
    )


    if query:

        # Previous conversation
        chat_history = (
            st.session_state.messages.copy()
        )


        # User message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )


        with st.chat_message("user"):

            st.markdown(query)


        # ------------------------------------------
        # Generate answer
        # ------------------------------------------

        with st.chat_message("assistant"):

            try:

                with st.spinner(
                    "Thinking..."
                ):

                    result = generate_answer(
                        query=query,
                        video_id=(
                            st.session_state.video_id
                        ),
                        chat_history=chat_history
                    )


                # Answer
                st.markdown(
                    result["answer"]
                )


                # ----------------------------------
                # Sources
                # ----------------------------------

                if result["sources"]:

                    st.markdown(
                        "### 📚 Sources"
                    )


                    for source in result["sources"]:

                        start = source["start"]
                        end = source["end"]
                        video_id = source["video_id"]

                        start_seconds = int(start)

                        youtube_link = (
                            "https://www.youtube.com/watch"
                            f"?v={video_id}"
                            f"&t={start_seconds}s"
                        )

                        start_minutes = int(
                            start // 60
                        )

                        start_secs = int(
                            start % 60
                        )

                        end_minutes = int(
                            end // 60
                        )

                        end_secs = int(
                            end % 60
                        )

                        start_time = (
                            f"{start_minutes:02d}:"
                            f"{start_secs:02d}"
                        )

                        end_time = (
                            f"{end_minutes:02d}:"
                            f"{end_secs:02d}"
                        )

                        st.markdown(
                            f"- 📍 "
                            f"[{start_time} – {end_time}]"
                            f"({youtube_link})"
                        )


                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["answer"]
                    }
                )


            except Exception as e:

                st.error(
                    f"❌ Failed to generate answer: "
                    f"{str(e)}"
                )