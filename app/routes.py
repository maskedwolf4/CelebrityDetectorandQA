from flask import Blueprint, render_template, request

from app.utils.image_handler import process_image
from app.utils.celebrity_detector import CelebrityDetector
from app.utils.qa_engine import QAEngine

import base64

main = Blueprint("main", __name__)

celebrity_detector = CelebrityDetector()
qa_engine = QAEngine()

@main.route("/", methods=["GET", "POST"])
def index():
    celeb_info = ""
    result_img_data = ""
    user_question = ""
    answer = ""
    
    if request.method == "POST":
        if "image" in request.files:
            image_file = request.files["image"]
            
            if image_file:
                img_bytes, face_box = process_image(image_file=image_file)
                
                celeb_info, celeb_name = celebrity_detector.identify(img_bytes)
                
                if face_box is not None:
                    result_img_data = base64.base64encode(img_bytes).decode()
                else:
                    celeb_info="No face detected. Plase Try another image"
                    
        elif "question" in request.form:
            user_question = request.form["question"]
            
            celeb_name = request.form["player_name"]
            celeb_info = request.form["player_info"]
            result_img_data = request.form["result_img_data"]
            
            answer = qa_engine.ask_about_celebrity(celeb_name, user_question)
            
    return render_template(
        "index.html",
        celeb_info=celeb_info,
        result_img_data=result_img_data,
        user_question=user_question,
        answer=answer
    )