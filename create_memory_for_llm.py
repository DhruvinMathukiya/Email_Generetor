import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

#Step 0: Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")


if not GOOGLE_API_KEY:
    raise ValueError(" GOOGLE_API_KEY not found in .env")
else:
    print(" Token loaded")

#Step 1: Load LLM 
def load_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.5,        
        max_output_tokens=2048,
        google_api_key=GOOGLE_API_KEY
    )

#Step 2: Prompt template
EMAIL_PROMPT_TEMPLATE = """
You are an elite professional email writer and communication strategist with expertise in corporate communication, networking emails, business outreach, client handling, follow-ups, HR communication, and executive correspondence.

Your task is to generate a highly personalized, professional, and natural-sounding email based on the sender’s personality, communication style, and the provided email request details.

━━━━━━━━━━━━━━━━━━━━━━
SENDER PROFILE (PERSON CONTEXT)
━━━━━━━━━━━━━━━━━━━━━━
The following information describes the sender’s personality, communication habits, profession, behavior, communication style, values, expertise, and professional background.

Use this information carefully to shape:
- writing style
- sentence structure
- tone
- vocabulary
- confidence level
- professionalism
- warmth
- empathy
- assertiveness
- persuasion level
- technical depth
- conversational style

SENDER DETAILS:
{person_context}

━━━━━━━━━━━━━━━━━━━━━━
EMAIL REQUEST DETAILS
━━━━━━━━━━━━━━━━━━━━━━

Recipient Name:
{recipient_name}

Recipient Role / Position:
{recipient_role}


Email Purpose:
{email_purpose}

Desired Tone:
{tone}

Key Points That Must Be Included:
{key_points}







━━━━━━━━━━━━━━━━━━━━━━
EMAIL WRITING INSTRUCTIONS
━━━━━━━━━━━━━━━━━━━━━━

1. PERSONALIZATION
- Make the email feel genuinely written by a real human.
- Adapt the language and writing style according to the sender’s personality and professional background.
- Use subtle personalization where appropriate.
- Avoid robotic or template-like phrasing.

2. TONE MATCHING
Strictly follow the requested tone:
- Professional
- Friendly
- Assertive
- Empathetic
- Formal
- Persuasive
- Confident
- Diplomatic
- Casual Professional
- Apologetic
- Appreciative
- Motivational

Blend tones naturally if multiple tones are provided.

3. EMAIL STRUCTURE
The email MUST include:
- Subject Line
- Professional Greeting
- Opening Paragraph
- Main Body
- Clear Call-To-Action
- Professional Closing
- Signature with sender name and designation

4. WRITING QUALITY
- Keep the flow smooth and coherent.
- Ensure clarity and readability.
- Avoid unnecessary repetition.
- Use concise but meaningful language.
- Maintain professionalism throughout.
- Make transitions between paragraphs natural.

5. CONTEXTUAL INTELLIGENCE
- Infer missing details intelligently when needed.
- If the purpose is business-related, maintain corporate professionalism.
- If the email is networking-oriented, make it warm and relationship-focused.
- If it is a complaint or escalation, make it firm but respectful.
- If it is a follow-up, ensure continuity and politeness.
- If it is sales or outreach, make it persuasive without sounding aggressive.

6. NATURAL HUMAN STYLE
- Avoid AI-like wording.
- Do NOT overuse buzzwords.
- Use realistic corporate communication language.
- Ensure the email sounds authentic and believable.

7. OUTPUT FORMAT
Generate ONLY the final email in the following format:

Subject: <subject line>

Dear/Hello <recipient name>,

<complete email body>

Best regards,
<sender name>
<sender job title>

━━━━━━━━━━━━━━━━━━━━━━
SPECIAL INSTRUCTIONS
━━━━━━━━━━━━━━━━━━━━━━

- If important information is missing, make reasonable professional assumptions.
- If the sender’s personality suggests a unique communication style, reflect it naturally.
- Prioritize professionalism, clarity, and authenticity.
- Ensure the final email is polished and ready to send without further editing.
- Do not explain the email.
- Do not include placeholders in the final response.
- Do not mention AI or prompt instructions.
- Make the email emotionally intelligent where appropriate.

Generate the complete email now.
"""

def set_email_prompt():
    return PromptTemplate(
        template=EMAIL_PROMPT_TEMPLATE,
        input_variables=[
            "person_context",
            "recipient_name",
            "recipient_role",
            "email_purpose",
            "tone",
            "key_points",
            "additional_notes"
        ]
    )

#  Step 3: Build chain 
def build_chain(person_context: dict = {}):
    llm = load_llm()
    prompt = set_email_prompt()

    # Format person dict into readable string
    if person_context:
        person_context_str = "\n".join(
            f"{k.replace('_', ' ').title()}: {v}"
            for k, v in person_context.items()
        )
    else:
        person_context_str = "No person details provided."

    chain = (
        {
            "person_context":   RunnablePassthrough() | (lambda _: person_context_str),
            "recipient_name":   RunnablePassthrough() | (lambda x: x["recipient_name"]),
            "recipient_role":   RunnablePassthrough() | (lambda x: x["recipient_role"]),
            "email_purpose":    RunnablePassthrough() | (lambda x: x["email_purpose"]),
            "tone":             RunnablePassthrough() | (lambda x: x["tone"]),
            "key_points":       RunnablePassthrough() | (lambda x: x["key_points"]),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

#  Step 4: Collect email details
def get_email_details():
    
    print("ENTER EMAIL DETAILS")

    print("\n Tone options: formal | friendly | assertive | empathetic | persuasive\n")

    email_details = {
        "recipient_name":   input("Recipient Name   : ").strip(),
        "recipient_role":   input("Recipient Role   : ").strip(),
        "email_purpose":    input("Email Purpose    : ").strip(),
        "tone":             input("Tone             : ").strip() or "formal",
        "key_points":       input("Key Points       : ").strip()
    }
    return email_details

# Step 5: Main
if __name__ == "__main__":

    # Collect person details
    print("        ENTER PERSON DETAILS (SENDER)")

    PERSON_CONTEXT = {
        "name":             input("Full Name        : ").strip(),
        "job_title":        input("Job Title        : ").strip(),
        "bio":              input("Bio              : ").strip(),
        "communication_style": input("Communication Style (e.g. formal, direct, warm): ").strip(),
        "personality":      input("Personality Traits (e.g. empathetic, assertive)  : ").strip(),
    }

    # Remove blank fields
    PERSON_CONTEXT = {k: v for k, v in PERSON_CONTEXT.items() if v}

    if not PERSON_CONTEXT:
        print("\n  No details entered. Continuing without person context.")

    print("\n Person details saved!")

    # Build chain once
    chain = build_chain(PERSON_CONTEXT)

    # Email generation loop
    print(" Email Generator Ready! Type 'exit' to quit.")

    while True:
        choice = input("\n Generate a new email? (yes/exit): ").strip().lower()

        if choice in ["exit", "quit", "no"]:
            print(" Goodbye!")
            break

        if choice != "yes":
            print("  Please type 'yes' or 'exit'.")
            continue

        # Get email details
        email_details = get_email_details()

        print("\n Generating email...\n")

        # Generate email
        result = chain.invoke(email_details)

        print(" GENERATED EMAIL:")

       
        print(result)
        