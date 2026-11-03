# Analyze the resumé content
import os
import requests
import json
from openai import OpenAI, RateLimitError, APIError
from fastapi import HTTPException
import re

MAX_RESUME_CHARS = int(os.getenv("MAX_RESUME_CHARS", 6000))
MAX_JD_CHARS = int(os.getenv("MAX_JD_CHARS", 6000))

class AIAnalyzer:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1/",
            api_key=os.getenv("GROQ_API_KEY"),
            max_retries=3
        )

    async def analyze_resume_with_ai(self, resume_text: str, jd: str):
        prompt = f"""Analyze this resume against the job description and respond with a JSON object.

RESUME: {resume_text[:MAX_RESUME_CHARS]}
JOB: {jd[:MAX_JD_CHARS]}

Respond with a JSON object in this exact format:
{{
  "matchPercentage": <number between 0-100>,
  "missingSkills": ["skill1", "skill2", "skill3"],
  "strengths": ["strength1", "strength2", "strength3"],
  "improvements": ["improvement1", "improvement2"],
  "summary": "A 2-3 sentence summary of the analysis"
}}"""

        try:
            print("=== CALLING AI API ===")
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a resume analyzer. Always respond with valid JSON only, no additional text."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content.strip()
            print("=== AI RESPONSE ===")
            print(content)
            print("=== PARSING JSON ===")
            parsed = json.loads(content)
            print("=== PARSED RESULT ===")
            print(parsed)
            return parsed

        except RateLimitError as e:
            print(f"Rate limited after retries: {e}")
            raise HTTPException(status_code=503, detail="The AI service is busy right now. Please try again in a minute.")
        except APIError as e:
            print(f"API Error {e}")
            raise HTTPException(status_code=502, detail="The AI service returned an error. Please try again.")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON from model: {e}")
            raise HTTPException(status_code=502, detail="The AI returned an unreadable response. Please try again.")
    
    def parse_response(self, text : str):
        parsed_response = {
            "matchPercentage": 60,
            "missingSkills": [],
            "strengths": [],
            "improvements": [],
            "summary": "",
        }
        try:
            # Match percentage - looking for number after "Match Percentage:**"
            match_p_pattern = r'(?i)\*\*Match Percentage:\*\*\s*(\d+)%?'
            match_percentage = re.search(match_p_pattern, text)
            if match_percentage:
                parsed_response["matchPercentage"] = int(match_percentage.group(1))

            # Missing Skills - extract bullet points between "Missing Skills:" and "Candidate Strengths:"
            missing_skills_pattern = r'(?i)\*\*Missing Skills:\*\*\s*\n((?:\*.*\n?)+)(?=\n*\d+\.\s*\*\*Candidate Strengths)'
            match_skills = re.search(missing_skills_pattern, text)
            if match_skills:
                skills_text = match_skills.group(1).split('\n')
                skills_list = [re.sub(r'^\*\s*', '', skill.strip())
                   for skill in skills_text if skill.strip() and skill.strip().startswith('*')]
                parsed_response["missingSkills"] = skills_list

            # Candidate Strengths - extract bullet points
            match_strengths_pattern = r'(?i)\*\*Candidate Strengths:\*\*\s*\n((?:\*.*\n?)+)(?=\n*\d+\.\s*\*\*Improvements)'
            match_strengths = re.search(match_strengths_pattern, text)
            if match_strengths:
                strengths_text = match_strengths.group(1).split('\n')
                strengths_list = [re.sub(r'^\*\s*', '', strength.strip())
                   for strength in strengths_text if strength.strip() and strength.strip().startswith('*')]
                parsed_response["strengths"] = strengths_list

            # Improvements - extract bullet points
            match_improvements_pattern = r'(?i)\*\*Improvements Needed:\*\*\s*\n((?:\*.*\n?)+)(?=\n*\d+\.\s*\*\*Overall)'
            match_improvements = re.search(match_improvements_pattern, text)
            if match_improvements:
                improvements_text = match_improvements.group(1).split('\n')
                improvements_list = [re.sub(r'^\*\s*', '', improvement.strip())
                   for improvement in improvements_text if improvement.strip() and improvement.strip().startswith('*')]
                parsed_response["improvements"] = improvements_list

            # Overall Summary - get text after "Overall Summary:**"
            match_summary_pattern = r'(?i)\*\*Overall Summary:\*\*\s*\n(.*?)(?=\n*$)'
            match_summary = re.search(match_summary_pattern, text, re.DOTALL)
            if match_summary:
                parsed_response["summary"] = match_summary.group(1).strip()

            return parsed_response
        except Exception as e:
            print(f"=== PARSING ERROR ===")
            print(f"Error: {e}")
            print(f"Response text (first 500 chars): {text[:500]}")
            return None
    
ai_analyzer = AIAnalyzer()