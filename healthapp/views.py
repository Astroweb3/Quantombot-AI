from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Data
from .serializers import DataSerializer
from rest_framework.response import Response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors 
from dotenv import load_dotenv
from configparser import ConfigParser
import os
import google.generativeai as genai

# Create your views here.
load_dotenv()

def index(request):
    return render(request, 'index.html')

def med(request,data):
    prompt = f"Generate a professional Response based:{data}"
    config = ConfigParser()
    config.read('F:/1.Project/_0Restapi/credentials.ini')
    api_key = config['GOOGLE_API_KEY']['google_api_key']
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k":1,
        "max_output_tokens":2048,
    }
    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    convo = model.start_chat(history=[
    ])

    convo.send_message(prompt)
    
    
    response = convo.last.text
    
    """response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role":"system","content":"you create medical documents based on treatment proposal data."},
            {"role":"user","content":prompt}
        ]
    )
    
    Text = response.choices[0].message.content"""
    
    Text = response
    """c = canvas.Canvas("prescription.pdf",pagesize = letter)
    c.setFillColor(colors.grey)
    
    c.drawString(50,700,"NebulaCare MedAI")
    
    c.setFillColor(colors.black)
    
    c.drawString(50,660, Text)

    c.save()"""
    
    a = {"context":Text}
    return render(request,"index.html",a)


@api_view(['POST'])
def postData(request):
    msg = str(request.POST["user-input"])
   
    dek = {"name":msg }
    serializer = DataSerializer(data = dek)
    if serializer.is_valid():
        serializer.save()
    return med(request,serializer.data)