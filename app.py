# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Configure your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Job model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Job {self.title}>'

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/jobs')
def jobs():
    all_jobs = Job.query.all()  # Get all job entries
    return render_template('jobs.html', jobs=all_jobs)

@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        if title and description:
            new_job = Job(title=title, description=description)
            db.session.add(new_job)
            db.session.commit()
            flash('Job added successfully!', 'success')
            return redirect(url_for('jobs'))
        else:
            flash('Please fill in all fields.', 'error')

    return render_template('add_job.html')

@app.route('/delete_job/<int:job_id>')
def delete_job(job_id):
    job_to_delete = Job.query.get_or_404(job_id)
    db.session.delete(job_to_delete)
    db.session.commit()
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('jobs'))

@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')

@app.route('/search_results', methods=['GET'])
def search_results():
    query = request.args.get('query')
    results = Job.query.filter(Job.title.ilike(f'%{query}%')).all()  # Case-insensitive search
    return render_template('search_results.html', jobs=results, query=query)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)