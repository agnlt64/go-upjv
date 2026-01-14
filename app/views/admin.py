from flask import Blueprint, render_template, request, redirect, flash, url_for
from app.models.user import User
from app.models.ride import Ride
from app import db
from sqlalchemy import or_, asc, desc
from flask_login import login_required, current_user

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
def admin_index():
    """Redirect to users page"""
    return redirect(url_for('admin.admin_users'))

@admin.route('/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('Unauthorized access', 'error')
        return redirect(url_for('main.index'))
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'asc')  # 'asc' or 'desc'
    search_query = request.args.get('q', '').strip()
    
    # Start building the query
    query = User.query
    
    # Apply search filter if search query exists
    if search_query:
        search_pattern = f'%{search_query}%'
        query = query.filter(
            or_(
                User.id.like(search_pattern),
                User.upjv_id.like(search_pattern),
                User.email.like(search_pattern),
                User.first_name.like(search_pattern),
                User.last_name.like(search_pattern),
                User.phone_number.like(search_pattern)
            )
        )
    
    # Apply sorting
    if sort == 'desc':
        query = query.order_by(desc(User.id))
    else:
        query = query.order_by(asc(User.id))
    
    # Paginate (10 users per page)
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    
    return render_template(
        'admin/users.html',
        pagination=pagination,
        sort=sort,
        search_query=search_query
    )

@admin.route('/reviews')
@login_required
def admin_reviews():
    if not current_user.is_admin:
        flash('Unauthorized access', 'error')
        return redirect(url_for('main.index'))
    
    # Get all rides that have reviews, sorted by date (most recent first)
    rides = Ride.query.filter(Ride.reviews.any()).order_by(desc(Ride.date)).all()
    
    return render_template('admin/reviews.html', rides=rides)