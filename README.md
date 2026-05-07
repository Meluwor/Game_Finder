Project Name: Game Finder

Functionality:
Game Finder is an AI-powered assistant that helps users discover video games through natural conversation.
It combines the reasoning capabilities of Large Language Models (LLMs) with the extensive RAWG Video Games Database
to provide accurate and personalized recommendations.


Technical Requirements & Setup:
To run this project locally, you need to configure your environment:API Keys:
    Obtain and add the following keys to your .env file:
        OPENAI_API_KEY:
            For the LLM logic (gpt-4o-mini).
        RAWG_API_KEY:
            To fetch real-time game metadata and imagery from the RAWG Video Games Database.
        FLASH_KEY:
            A custom secret key for session security and encryption.

Data Persistence & Memory Architecture:
The project uses a hybrid approach to data management to balance long-term personalization
with session-based privacy:
    Persistent SQLite Database (Long-Term Storage):
    Your core profile and selected "favorites" are stored in a local SQLite file.
    This ensures that your identified gaming preferences survive application restarts and
    can be used as a foundation for future recommendations.
    Volatile Chat Memory (Session-Based):
    The immediate conversation history with the LLM is currently handled in-memory (RAM).
    While the AI "remembers" what you said two minutes ago during the active session,
    the chat history is not saved to the database. Starting a new session provides a clean slate
    for the AI's conversational context.