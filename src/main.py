from flask import Blueprint,render_template,Flask,request,redirect,url_for,flash,current_app,jsonify
from flask_login import login_required,current_user
from werkzeug.security import check_password_hash
from .models import User,User_Detail,Service,Project
import os,secrets
from . import db
from werkzeug.utils import secure_filename
from flask import current_app
from flask import request, jsonify, make_response
from flask import Flask, send_from_directory
from flask_mail import Mail,Message
from flask import current_app

main = Blueprint('main', __name__)

@main.route('/send_email', methods=['POST'])
def send_email_endpoint():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        message_body = f"Sender Name: {name}\nSender Email: {email}\nSubject: {subject}\nMessage: {message}"
        send_email(name, email, subject, message_body)
        return jsonify({'message': 'Email sent successfully'}), 200

def send_email(name, email, subject, message):
    mail = current_app.extensions['mail'] 
    msg = Message(subject, sender=email, recipients=['sabir99918@gmail.com'], body=message)
    mail.send(msg)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}

def generate_random_filename(filename):
    _, extension = os.path.splitext(filename)
    random_hex = secrets.token_hex(8)
    new_filename = random_hex + extension
    return new_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/user_detail', methods=['POST'])
def create_user_detail():
    if 'profile' in request.files:
        file = request.files['profile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_filename = generate_random_filename(filename)
            relative_path = f'{new_filename}'
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename))
        else:
            return jsonify({'message': 'Invalid file format for image upload'}), 400
    else:
        relative_path = None
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.json
        print(data)
    elif content_type.startswith('multipart/form-data') or content_type.startswith('application/x-www-form-urlencoded'):
        data = request.form.to_dict(flat=True)
        print(data)
    else:
        return make_response(jsonify({'message': 'Unsupported Content-Type'}), 415)
    data['profile'] = relative_path
    user_detail = User_Detail(**data)
    db.session.add(user_detail)
    db.session.commit()
    return jsonify({'message': 'User detail created successfully'}), 201

@main.route('/service', methods=['POST'])
def create_service():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.json
    elif content_type.startswith('multipart/form-data') or content_type.startswith('application/x-www-form-urlencoded'):
        data = request.form.to_dict(flat=True)
    else:
        return make_response(jsonify({'message': 'Unsupported Content-Type'}), 415)
    service = Service(**data)
    db.session.add(service)
    db.session.commit()
    return jsonify({'message': 'Service created successfully'}), 201


@main.route('/project', methods=['POST'])
def create_project():
    if 'images' in request.files:
        file = request.files['images']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_filename = generate_random_filename(filename)
            relative_path = f'{new_filename}'
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename))
        else:
            return jsonify({'message': 'Invalid file format for image upload'}), 400
    else:
        relative_path = None
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.json
    elif content_type.startswith('multipart/form-data') or content_type.startswith('application/x-www-form-urlencoded'):
        data = request.form.to_dict(flat=True)
    else:
        return make_response(jsonify({'message': 'Unsupported Content-Type'}), 415)
    data['images'] = relative_path
    project = Project(**data)
    db.session.add(project)
    db.session.commit()
    return jsonify({'message': 'Project created successfully'}), 201


@main.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('src/static/images', filename)


@main.route('/user_detail', methods=['GET'])
def get_user_details():
    user_details = User_Detail.query.all()
    user_details_data = [{'id': detail.id, 'name': detail.name, 'profession': detail.profession, 'description': detail.description,
                          'profile': detail.profile, 'facebook': detail.facebook, 'linkedin': detail.linkedin,
                          'instagram': detail.instagram, 'twitter': detail.twitter, 'github': detail.github,
                          'cv': detail.cv, 'detailed_description': detail.detailed_description} for detail in user_details]
    print(jsonify(user_details_data))
    return jsonify(user_details_data)


@main.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    services_data = [{'id': service.id, 'title': service.title, 'description': service.description, 'link': service.link}
                     for service in services]
    return jsonify(services_data)


@main.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    projects_data = [{'id': project.id,'name':project.name , 'images': project.images, 'short_description': project.short_description,
                      'project_link': project.project_link} for project in projects]
    return jsonify(projects_data)


@main.route('/user_details/<int:id>', methods=['PATCH'])
def update_user_detail(id):
    user_detail = User_Detail.query.get(id)
    if not user_detail:
        return jsonify({'message': 'User detail not found'}), 404
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.json
        print("Data received from frontend:", data)  # Print the received data

    elif content_type.startswith('multipart/form-data') or content_type.startswith('application/x-www-form-urlencoded'):
        data = request.form.to_dict(flat=True)
    else:
        return make_response(jsonify({'message': 'Unsupported Content-Type'}), 415)

    for key, value in data.items():
        setattr(user_detail, key, value)
    
    db.session.commit()
    
    user_detail_data = {
        'id': user_detail.id,
        'name': user_detail.name,
        'profession': user_detail.profession,
        'facebook': user_detail.facebook,
        'linkedin': user_detail.linkedin,
        'github':user_detail.github,
        'instagram':user_detail.instagram,
        'cv':user_detail.cv,
        'profile': user_detail.profile,
        'twitter':user_detail.twitter,
        'description':user_detail.detailed_description
    }
    
    return jsonify(user_detail_data)


@main.route('/user_profile/<int:id>', methods=['PATCH'])
def update_user_profile(id):
    user_detail = User_Detail.query.get(id)
    if not user_detail:
        return jsonify({'error': 'User detail not found'}), 404
    
    profile_file = request.files.get('profile')
    cv_file = request.files.get('cv')
    
    # Check if profile image is provided
    if profile_file and profile_file.filename != '':
        if allowed_file(profile_file.filename):
            profile_filename = secure_filename(profile_file.filename)
            profile_new_filename = generate_random_filename(profile_filename)
            profile_relative_path = os.path.join(current_app.config['UPLOAD_FOLDER'], profile_new_filename)
            profile_file.save(profile_relative_path)
            user_detail.profile = profile_new_filename
        else:
            return jsonify({'error': 'Invalid file format for profile image upload'}), 400
    
    # Check if CV is provided
    if cv_file and cv_file.filename != '':
        if allowed_file(cv_file.filename):
            cv_filename = secure_filename(cv_file.filename)
            cv_new_filename = generate_random_filename(cv_filename)
            cv_relative_path = os.path.join(current_app.config['UPLOAD_FOLDER'], cv_new_filename)
            cv_file.save(cv_relative_path)
            user_detail.cv = cv_new_filename
        else:
            return jsonify({'error': 'Invalid file format for CV upload'}), 400

    db.session.commit()

    return jsonify({
        'message': 'Profile and/or CV updated successfully',
        'user_detail': {
            'id': user_detail.id,
            'name': user_detail.name,
            'profession': user_detail.profession,
            'facebook': user_detail.facebook,
            'linkedin': user_detail.linkedin,
            'github': user_detail.github,
            'instagram': user_detail.instagram,
            'cv': user_detail.cv,
            'profile': user_detail.profile,
            'twitter': user_detail.twitter,
            'description': user_detail.detailed_description
        }
    }), 200


@main.route('/services/<int:id>', methods=['PATCH'])
def update_service(id):
    service = Service.query.get(id)
    if not service:
        return jsonify({'message': 'Service not found'}), 404
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.json
    elif content_type.startswith('multipart/form-data') or content_type.startswith('application/x-www-form-urlencoded'):
        data = request.form.to_dict(flat=True)
    else:
        return make_response(jsonify({'message': 'Unsupported Content-Type'}), 415)
    for key, value in data.items():
        setattr(service, key, value)

    db.session.commit()
    service_data = {'id': service.id, 'title': service.title, 'description': service.description, 'link': service.link}
    return jsonify(service_data)

@main.route('/projects/<int:id>', methods=['PATCH'])
def update_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    
    # Handle image upload
    image_file = request.files.get('images')
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        new_filename = generate_random_filename(filename)
        relative_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
        image_file.save(relative_path)
        project.images= new_filename
    
    # Update other project details
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.json
    elif content_type.startswith('multipart/form-data') or content_type.startswith('application/x-www-form-urlencoded'):
        data = request.form.to_dict(flat=True)
    else:
        return make_response(jsonify({'message': 'Unsupported Content-Type'}), 415)
    
    for key, value in data.items():
        setattr(project, key, value)
    
    db.session.commit()
    
    project_data = {
        'id': project.id,
        'image': project.images,  
        'short_description': project.short_description,
        'project_link': project.project_link,
    }
    return jsonify(project_data)




@main.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'}), 200

@main.route('/services/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = Service.query.get(id)
    if not service:
        return jsonify({'message': 'Service not found'}), 404
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted successfully'}), 200
