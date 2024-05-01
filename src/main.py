from flask import Blueprint,render_template,Flask,request,redirect,url_for,flash,current_app,jsonify
from flask_login import login_required,current_user
from werkzeug.security import check_password_hash
from .models import User,User_Detail,Service,Project,Contact
import os,secrets
from . import db
from werkzeug.utils import secure_filename
from flask import current_app
from flask import request, jsonify, make_response
from flask import Flask, send_from_directory



main=Blueprint('main',__name__)


@main.route('/')
def index():
    return render_template('login.html')

@main.route('/profile')
@login_required
def profile():
    is_logged_out = False  
    if not current_user.is_authenticated:
        is_logged_out = True
    return render_template('profile.html',username=current_user.username,is_logged_out=is_logged_out)

@main.route('/change_password')
def change_password():
    return render_template('change_password.html')
    
@main.route('/change_password',methods=['GET','POST'])
def change_password_post():
    if request.method=='POST':
        current_password=request.form.get('current_password')
        new_password=request.form.get('new_password')
        if not check_password_hash(current_user.password,current_password):
            flash('current password is incorrect','error')

        else:
            current_user.set_password(new_password)
            session=db.session
            session.commit()
            return redirect('/profile')
        
    return render_template('change_password.html')

@main.route('/change_username',methods=['POST'])
def change_username():
    if request.method=='POST':
        new_username=request.form.get('new_username')
        current_user.set_username(new_username)
        session=db.session
        session.commit()
        return redirect('/profile')

@main.route('/change_email',methods=['POST'])
def change_email():
    if request.method=='POST':
        new_email=request.form.get('new_email')
        current_user.set_email(new_email)
        session=db.session
        session.commit()
        return redirect('/profile')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def generate_random_filename(filename):
    _, extension = os.path.splitext(filename)
    random_hex = secrets.token_hex(8)
    new_filename = random_hex + extension
    return new_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/upload_profile', methods=['POST'])
def profile_update():
    app = current_app
    if 'picture' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)
    file = request.files['picture']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        fn = generate_random_filename(filename)
        relative_path = f'images/{fn}' 
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
        user = User.query.get(current_user.id)
        user.picture = relative_path
        db.session.commit()
    return redirect(url_for('main.profile'))

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



@main.route('/contact', methods=['POST'])
def create_contact():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.json
    elif content_type.startswith('multipart/form-data') or content_type.startswith('application/x-www-form-urlencoded'):
        data = request.form.to_dict(flat=True)
    else:
        return make_response(jsonify({'message': 'Unsupported Content-Type'}), 415)
    contact = Contact(**data)
    db.session.add(contact)
    db.session.commit()
    return jsonify({'message': 'Contact created successfully'}), 201

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
    projects_data = [{'id': project.id, 'images': project.images, 'short_description': project.short_description,
                      'project_link': project.project_link} for project in projects]
    return jsonify(projects_data)


@main.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    contacts_data = [{'id': contact.id, 'name': contact.name, 'email': contact.email, 'phone': contact.phone,
                      'subject': contact.subject, 'message': contact.message} for contact in contacts]
    return jsonify(contacts_data)


@main.route('/user_details/<int:id>', methods=['PATCH'])
def update_user_detail(id):
    user_detail = User_Detail.query.get(id)
    if not user_detail:
        return jsonify({'message': 'User detail not found'}), 404
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.json
    elif content_type.startswith('multipart/form-data') or content_type.startswith('application/x-www-form-urlencoded'):
        data = request.form.to_dict(flat=True)
    else:
        return make_response(jsonify({'message': 'Unsupported Content-Type'}), 415)
    for key, value in data.items():
        setattr(user_detail, key, value)
    db.session.commit()
    user_detail_data = {'id': user_detail.id, 'name': user_detail.name, 'profession': user_detail.profession, 
                        'description': user_detail.description, 'profile': user_detail.profile, 
                        'facebook': user_detail.facebook, 'linkedin': user_detail.linkedin, 
                        'instagram': user_detail.instagram, 'twitter': user_detail.twitter, 
                        'github': user_detail.github, 'cv': user_detail.cv, 
                        'detailed_description': user_detail.detailed_description}
    return jsonify(user_detail_data)


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
    project_data = {'id': project.id, 'images': project.images, 'short_description': project.short_description,
                    'project_link': project.project_link}
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
