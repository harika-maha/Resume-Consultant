# Analyze the resumé content
import os
import requests
import json
from openai import OpenAI
import re

class AIAnalyzer:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1/",
            api_key=os.getenv("GROQ_API_KEY")
        )

    async def analyze_resume_with_ai(self, resume_text: str, jd: str):
        prompt = f"""Analyze this resume against the job description:

                    RESUME: {resume_text[:800]}
                    JOB: {jd[:800]}

                    Provide:
                    1. Match percentage (0-100)
                    2. Missing skills (list 3-5)
                    3. Candidate strengths (list 3-5) 
                    4. Improvements needed (list 2-3)
                    5. Overall summary (2 sentences)"""
        
        try:
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content.strip()
            # print(self.parse_response(content))
            return self.parse_response(content)
        
        except Exception as e:
            print(f"API Error {e}")
        return {
            "matchPercentage": 40,
            "missingSkills": ["API failed - manual review needed"],
            "strengths": ["Technical background"],
            "improvements": ["Review job requirements manually"],
            "summary": "Analysis unavailable - please try again"
        }
    
    def parse_response(self, text : str):
        parsed_response = {
            "matchPercentage": 60,
            "missingSkills": [],
            "strengths": [],
            "improvements": [],
            "summary": "",
        }
        try:
            # print("-"*10)
            # print(text[:300])
            # print("-"*10)
            match_p_pattern = r'(?i)match percentage.*?:\D*(\d+)'
            match_percentage = re.search(match_p_pattern, text)
            # print(match_percentage.group(1))      #PRINT STATEMENT
            percentage = match_percentage.group(1)
            parsed_response["matchPercentage"] = int(percentage)


            missing_skills_pattern = r'(?i)missing skills?.*:.*\n*((?:.*\n)*?)(?=(?:\*\*)?\d*\.*\s*Candidate strengths)'
            match_skills = re.search(missing_skills_pattern, text)
            # print(match_skills.group(1))          #PRINT STATEMENT
            skills_text = match_skills.group(1).split('\n')
            skills_list = [re.sub(r'^[\d\-\*\•]+\.?\s*', '', skill.strip()) 
               for skill in skills_text if skill.strip()]
            # print(skills_list)
            parsed_response["missingSkills"] = skills_list


            match_strengths_pattern = r'(?i)Candidate strengths.*:.*\n((?:.*\n*)*?)(?=(?:\*\*)?(\d\.\s)?Improvements?)'
            match_strengths = re.search(match_strengths_pattern, text)
            strengths_text = match_strengths.group(1).split('\n')
            strengths_list = [re.sub(r'^[\d\-\*\•]+\.?\s*', '', strength.strip()) 
               for strength in strengths_text if strength.strip()]
            parsed_response["strengths"] = strengths_list
            # print(match_strengths.group(1))           #PRINT STATEMENT


            match_improvements_pattern = r'(?i)improvements.*\n((?:.*\n*)*?)(?=(\*\*)?(\d.\s)?Overall)'
            match_improvements = re.search(match_improvements_pattern, text)
            improvements_text = match_improvements.group(1).split('\n')
            improvements_list = [re.sub(r'^[\d\-\*\•]+\.?\s*', '', improvement.strip()) 
               for improvement in improvements_text if improvement.strip()]
            parsed_response["improvements"] = improvements_list
            # print(str(match_improvements.group(1)))           #PRINT STATEMENT


            match_summary_pattern = r'(?i)overall.*:(?:\*\*)?\s*(.*?)(?=\n\n|$)'
            match_summary = re.search(match_summary_pattern, text)
            # print(match_summary)          #PRINT STATEMENT
            parsed_response["summary"] = str(match_summary.group(1))
            # print(str(match_summary.group(1)))            #PRINT STATEMENT
            return parsed_response
        except Exception as e:
            print(e)
    
ai_analyzer = AIAnalyzer()