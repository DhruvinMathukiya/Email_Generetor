import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load API Key
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print(" GOOGLE_API_KEY not found!")
    exit()

print(" Token loaded successfully!\n")

# PERSON DETAILS

def get_person_details():
    print("ENTER PERSON DETAILS")

    full_name = input("Full Name        : ")
    job_title = input("Job Title        : ")
    bio = input("Bio              : ")
    communication_style = input("Communication Style : ")
    personality_traits = input("Personality Traits  : ")

    return {
        "full_name": full_name,
        "job_title": job_title,
        "bio": bio,
        "communication_style": communication_style,
        "personality_traits": personality_traits
    }


# SUMMARY DETAILS

def get_summary_details():
    print("ENTER SUMMARY DETAILS")

    topic = input("Topic             : ")
    key_points = input("Key Points        : ")
    tone = input("Tone              : ")
    summary_length = input("Summary Length (short/medium/long): ")

    return {
        "topic": topic,
        "key_points": key_points,
        "tone": tone,
        "summary_length": summary_length
    }


# LLM SETUP

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# PROMPT TEMPLATE

template = """
You are an expert professional summary writer with advanced skills in business communication, content structuring, and personalized writing.

Your task is to generate a highly detailed, professional, well-structured, and descriptive summary based on the provided person details and summary requirements.

PERSON DETAILS:
Name: {full_name}
Job Title: {job_title}
Bio: {bio}
Communication Style: {communication_style}
Personality Traits: {personality_traits}

SUMMARY DETAILS:
Topic: {topic}
Key Points: {key_points}
Tone: {tone}
Summary Length: {summary_length}

INSTRUCTIONS:

- Create a comprehensive and detailed professional summary.
- The summary should strongly reflect the person's personality, communication style, technical background, and expertise.
- Expand naturally on the provided key points with meaningful explanations and contextual depth.
- Write in a polished, human-like, and professional manner.
- Ensure the tone remains fully consistent throughout the summary.
- Highlight strengths, skills, experience, interests, goals, and professional qualities naturally within the content.
- Make the writing engaging, descriptive, and informative instead of short or generic.
- Use clear structure, logical flow, and professional vocabulary.
- Include relevant insights about technical capabilities, learning mindset, problem-solving ability, collaboration style, and professional interests whenever appropriate.
- Adapt the language style according to the communication style and personality traits provided.
- If the summary length is "long", generate a detailed multi-paragraph summary with rich explanations and elaboration.
- Avoid repetitive statements.
- Avoid bullet points unless absolutely necessary.
- Generate content that sounds natural and realistic, not robotic.
- Focus on clarity, professionalism, readability, and depth.

OUTPUT REQUIREMENTS:
- Generate only the final summary.
- Do not include headings, labels, notes, or explanations.
- The output should be presentation-ready and professional.

Now generate the detailed professional summary.
"""

prompt = PromptTemplate(
    input_variables=[
        "full_name",
        "job_title",
        "bio",
        "communication_style",
        "personality_traits",
        "topic",
        "key_points",
        "tone",
        "summary_length"
    ],
    template=template
)

# CHAIN

chain = prompt | llm | StrOutputParser()

# MAIN PROGRAM

person_details = get_person_details()

print("\n Person details saved!")

while True:
    choice = input("\nGenerate a summary? (yes/exit): ").lower()

    if choice == "exit":
        print("\n Exiting program...")
        break

    elif choice == "yes":

        summary_details = get_summary_details()

        # Merge dictionaries
        final_input = {
            **person_details,
            **summary_details
        }

        print("\n Generating summary...\n")

        result = chain.invoke(final_input)

        print("GENERATED SUMMARY")
        print(result)

    else:
        print(" Invalid input! Type 'yes' or 'exit'.")