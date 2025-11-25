# Example interactions (sample outputs)

These examples illustrate expected behavior when running the Streamlit UI.

1) Summarization Mode

Input prompt: "Summarize overall sales performance and key outliers"

Output (example):
"Overall sales grew 2.5% YoY, led by the West region and Widgets product line. Accessories underperformed in Q4, with a 15% decline compared to Q3. Top categories were Hardware and Electronics."

2) Conversational Q&A Mode

Question: "Which product line underperformed in Q4?"

Answer (example):
"Accessories — showed the largest decrease in total sales for Q4 vs Q3. Recommend detailed inventory review and promotional push."

Note: The LLM-backed responses will be richer when you provide OPENAI_API_KEY or GEMINI_API_KEY. Without a key the system uses a deterministic offline fallback that still surfaces data-driven answers.
